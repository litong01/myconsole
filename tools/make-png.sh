#!/usr/bin/env bash
# Render icons/*.svg to icons/png/*.png (256x256, transparent) using headless Chrome.
# Only needed if you edit the SVGs; the PNGs are committed.
set -euo pipefail

CHROME="${CHROME:-/Applications/Google Chrome.app/Contents/MacOS/Google Chrome}"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SIZE="${SIZE:-256}"
OUT="$ROOT/icons/png"

if [ ! -x "$CHROME" ]; then
  echo "Chrome not found at: $CHROME" >&2
  echo "Set CHROME=/path/to/chrome and retry." >&2
  exit 1
fi

mkdir -p "$OUT"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

for svg in "$ROOT"/icons/*.svg; do
  name="$(basename "$svg" .svg)"
  cat > "$TMP/$name.html" <<HTML
<!DOCTYPE html>
<meta charset="utf-8">
<style>
  html, body { margin: 0; background: transparent; }
  img { display: block; width: ${SIZE}px; height: ${SIZE}px; }
</style>
<img src="file://$svg" alt="">
HTML

  "$CHROME" \
    --headless \
    --disable-gpu \
    --hide-scrollbars \
    --default-background-color=00000000 \
    --force-device-scale-factor=1 \
    --window-size="$SIZE,$SIZE" \
    --screenshot="$OUT/$name.png" \
    "file://$TMP/$name.html" >/dev/null 2>&1

  echo "rendered $name.png"
done

echo "PNGs written to icons/png (${SIZE}x${SIZE})"
