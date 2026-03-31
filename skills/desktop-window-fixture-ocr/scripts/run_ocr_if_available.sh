#!/usr/bin/env bash
set -euo pipefail

image_path="${1:-}"
if [[ -z "${image_path}" ]]; then
  echo "usage: $0 <image>" >&2
  exit 2
fi

if command -v tesseract >/dev/null 2>&1; then
  exec tesseract "${image_path}" stdout
fi

echo "tesseract is not installed; OCR unavailable for ${image_path}" >&2
exit 0
