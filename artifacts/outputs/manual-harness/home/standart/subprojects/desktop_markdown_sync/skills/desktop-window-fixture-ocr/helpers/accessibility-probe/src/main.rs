use std::env;
use std::process::{Command, Stdio};

fn run(args: &[&str]) -> Result<String, String> {
    let output = Command::new(args[0])
        .args(&args[1..])
        .stdin(Stdio::null())
        .output()
        .map_err(|err| format!("failed to spawn {}: {err}", args[0]))?;
    if !output.status.success() {
        return Err(String::from_utf8_lossy(&output.stderr).trim().to_string());
    }
    Ok(String::from_utf8_lossy(&output.stdout).trim().to_string())
}

fn escape_json(value: &str) -> String {
    value
        .replace('\\', "\\\\")
        .replace('"', "\\\"")
        .replace('\n', "\\n")
}

fn print_status() -> Result<(), String> {
    let enabled = run(&[
        "gdbus",
        "call",
        "--session",
        "--dest",
        "org.a11y.Bus",
        "--object-path",
        "/org/a11y/bus",
        "--method",
        "org.freedesktop.DBus.Properties.Get",
        "org.a11y.Status",
        "IsEnabled",
    ])?;
    let screen_reader_enabled = run(&[
        "gdbus",
        "call",
        "--session",
        "--dest",
        "org.a11y.Bus",
        "--object-path",
        "/org/a11y/bus",
        "--method",
        "org.freedesktop.DBus.Properties.Get",
        "org.a11y.Status",
        "ScreenReaderEnabled",
    ])?;
    let bus_address = run(&[
        "gdbus",
        "call",
        "--session",
        "--dest",
        "org.a11y.Bus",
        "--object-path",
        "/org/a11y/bus",
        "--method",
        "org.a11y.Bus.GetAddress",
    ])?;
    println!(
        "{{\n  \"is_enabled_raw\": \"{}\",\n  \"screen_reader_enabled_raw\": \"{}\",\n  \"bus_address_raw\": \"{}\"\n}}",
        escape_json(&enabled),
        escape_json(&screen_reader_enabled),
        escape_json(&bus_address),
    );
    Ok(())
}

fn print_labels(service: &str, path: &str) -> Result<(), String> {
    let name = run(&[
        "gdbus",
        "call",
        "--session",
        "--dest",
        service,
        "--object-path",
        path,
        "--method",
        "org.freedesktop.DBus.Properties.Get",
        "org.a11y.atspi.Accessible",
        "Name",
    ])?;
    let description = run(&[
        "gdbus",
        "call",
        "--session",
        "--dest",
        service,
        "--object-path",
        path,
        "--method",
        "org.freedesktop.DBus.Properties.Get",
        "org.a11y.atspi.Accessible",
        "Description",
    ])?;
    let child_count = run(&[
        "gdbus",
        "call",
        "--session",
        "--dest",
        service,
        "--object-path",
        path,
        "--method",
        "org.freedesktop.DBus.Properties.Get",
        "org.a11y.atspi.Accessible",
        "ChildCount",
    ])?;
    println!(
        "{{\n  \"service\": \"{}\",\n  \"path\": \"{}\",\n  \"name_raw\": \"{}\",\n  \"description_raw\": \"{}\",\n  \"child_count_raw\": \"{}\"\n}}",
        escape_json(service),
        escape_json(path),
        escape_json(&name),
        escape_json(&description),
        escape_json(&child_count),
    );
    Ok(())
}

fn usage() -> ! {
    eprintln!("usage: accessibility-probe <status|labels> [service path]");
    std::process::exit(2);
}

fn main() -> Result<(), String> {
    let mut args = env::args().skip(1);
    match args.next().as_deref() {
        Some("status") => print_status(),
        Some("labels") => {
            let service = args.next().unwrap_or_else(|| usage());
            let path = args.next().unwrap_or_else(|| usage());
            print_labels(&service, &path)
        }
        _ => usage(),
    }
}

#[cfg(test)]
mod tests {
    use super::escape_json;

    #[test]
    fn escapes_quotes_and_newlines() {
        assert_eq!(escape_json("a\"b\nc"), "a\\\"b\\nc");
    }
}
