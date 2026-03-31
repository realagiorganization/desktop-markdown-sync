use serde::Serialize;
use std::env;
use zbus::blocking::{Connection, Proxy};

#[derive(Serialize)]
struct StatusOutput {
    is_enabled: bool,
    screen_reader_enabled: bool,
    bus_address: String,
}

#[derive(Serialize)]
struct LabelOutput {
    service: String,
    path: String,
    name: String,
    description: String,
    role_name: String,
    child_count: i32,
}

fn status() -> Result<(), Box<dyn std::error::Error>> {
    let connection = Connection::session()?;
    let status = Proxy::new(&connection, "org.a11y.Bus", "/org/a11y/bus", "org.a11y.Status")?;
    let bus = Proxy::new(&connection, "org.a11y.Bus", "/org/a11y/bus", "org.a11y.Bus")?;
    let is_enabled: bool = status.get_property("IsEnabled")?;
    let screen_reader_enabled: bool = status.get_property("ScreenReaderEnabled")?;
    let bus_address: String = bus.call("GetAddress", &())?;
    let output = StatusOutput {
        is_enabled,
        screen_reader_enabled,
        bus_address,
    };
    println!("{}", serde_json::to_string_pretty(&output)?);
    Ok(())
}

fn labels(service: &str, path: &str) -> Result<(), Box<dyn std::error::Error>> {
    let connection = Connection::session()?;
    let accessible = Proxy::new(
        &connection,
        service,
        path,
        "org.a11y.atspi.Accessible",
    )?;
    let name: String = accessible.get_property("Name")?;
    let description: String = accessible.get_property("Description")?;
    let child_count: i32 = accessible.get_property("ChildCount")?;
    let role_name: String = accessible.call("GetRoleName", &())?;
    let output = LabelOutput {
        service: service.to_string(),
        path: path.to_string(),
        name,
        description,
        role_name,
        child_count,
    };
    println!("{}", serde_json::to_string_pretty(&output)?);
    Ok(())
}

fn usage() -> ! {
    eprintln!("usage: accessibility-probe <status|labels> [service path]");
    std::process::exit(2);
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let mut args = env::args().skip(1);
    match args.next().as_deref() {
        Some("status") => status(),
        Some("labels") => {
            let service = args.next().unwrap_or_else(|| usage());
            let path = args.next().unwrap_or_else(|| usage());
            labels(&service, &path)
        }
        _ => usage(),
    }
}
