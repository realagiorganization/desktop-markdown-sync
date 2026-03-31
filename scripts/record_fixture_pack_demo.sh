#!/usr/bin/env bash
set -euo pipefail

manifest_path="${1:?manifest path required}"
output_path="${2:?output path required}"

mkdir -p "$(dirname "${output_path}")"
rm -f "${output_path}"

display_id="${DISPLAY:-:99}"
export DISPLAY="${display_id}"

Xvfb "${DISPLAY}" -screen 0 1280x720x24 >/tmp/desktop_markdown_sync_xvfb.log 2>&1 &
xvfb_pid=$!

cleanup() {
  kill "${ffmpeg_pid:-}" "${app_pid:-}" "${xvfb_pid:-}" 2>/dev/null || true
}
trap cleanup EXIT

sleep 1
python3 scripts/fixture_pack_demo_app.py --manifest "${manifest_path}" --cycles 3 --linger-ms 900 &
app_pid=$!

sleep 1
ffmpeg -y \
  -video_size 1280x720 \
  -framerate 12 \
  -f x11grab \
  -i "${DISPLAY}" \
  -pix_fmt yuv420p \
  -t 10 \
  "${output_path}" \
  >/tmp/desktop_markdown_sync_ffmpeg.log 2>&1 &
ffmpeg_pid=$!

wait "${app_pid}"
wait "${ffmpeg_pid}"
