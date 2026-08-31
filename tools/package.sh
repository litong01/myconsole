#!/usr/bin/env bash
# Build myconsole.zip for the tablet: unzip to /sdcard/myconsole/
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DIST="$ROOT/dist"
STAGE="$DIST/myconsole"

rm -rf "$DIST"
mkdir -p "$STAGE"

cp "$ROOT/README.md" "$STAGE/"
cp -R "$ROOT/inject" "$STAGE/inject"
cp -R "$ROOT/icons" "$STAGE/icons"
cp -R "$ROOT/fkb" "$STAGE/fkb"

# Keep the zip tablet-only: no preview, tools, or GitHub metadata.
find "$STAGE" -name '.DS_Store' -delete

(
  cd "$DIST"
  zip -r -q myconsole.zip myconsole
)

echo "Wrote $DIST/myconsole.zip"
unzip -l "$DIST/myconsole.zip" | sed -n '1,80p'
