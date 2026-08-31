#!/usr/bin/env python3
"""Render icons/png/*.png into the theme's circular wells for comparison.

    python3 tools/icon-sheet.py /tmp/sheet.png [label]

The first row is the trio that has to look even next to each other; the rest of
the set follows.
"""

import pathlib
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

TRIO = ["streaming", "router", "switch"]
REST = ["wifi", "nas", "server", "firewall", "camera", "dashboard", "default"]

PAGE = """<!DOCTYPE html>
<meta charset="utf-8">
<style>
  html, body { margin: 0; background: #0b0b0c; color: #e8eaed;
               font: 14px system-ui, sans-serif; }
  .wrap { padding: 28px 24px 32px; }
  h2 { margin: 0 0 14px; font-size: 13px; font-weight: 400;
       color: rgba(232,234,237,0.6); letter-spacing: 0.04em; }
  .row { display: flex; gap: 28px; margin-bottom: 30px; }
  .tile { width: 132px; text-align: center; }
  .well { width: 132px; height: 132px; padding: 18px; box-sizing: border-box;
          border-radius: 50%%; border: 1px solid rgba(255,255,255,0.09);
          background: radial-gradient(circle at 35%% 28%%, rgba(255,255,255,0.08),
                      rgba(255,255,255,0.02) 55%%, rgba(0,0,0,0.15) 100%%), #141416;
          display: flex; align-items: center; justify-content: center;
          position: relative; }
  /* Guides: same box on every tile, to expose uneven artwork */
  .well::after { content: ""; position: absolute; left: 50%%; top: 50%%;
                 width: 84px; height: 84px; transform: translate(-50%%, -50%%);
                 outline: 1px dashed rgba(138,180,248,0.35); }
  .well img { width: 100%%; height: 100%%; object-fit: contain; }
  .tile span { display: block; margin-top: 4px; font-size: 1.05rem;
               color: rgba(232,234,237,0.72); }
  .tag { position: fixed; bottom: 8px; right: 12px; font-size: 12px;
         color: rgba(232,234,237,0.45); }
</style>
<div class="wrap">
  <h2>side by side — dashed box is identical on every tile</h2>
  <div class="row">%s</div>
  <div class="row">%s</div>
</div>
<div class="tag">%s</div>
"""


def tiles(names: list[str]) -> str:
    out = []
    for name in names:
        png = ROOT / "icons" / "png" / f"{name}.png"
        out.append(
            f'<div class="tile"><div class="well">'
            f'<img src="file://{png}"></div><span>{name}</span></div>'
        )
    return "\n".join(out)


def main() -> int:
    out = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "/tmp/icon-sheet.png")
    label = sys.argv[2] if len(sys.argv) > 2 else ""

    with tempfile.TemporaryDirectory() as tmp:
        page = pathlib.Path(tmp) / "sheet.html"
        page.write_text(PAGE % (tiles(TRIO), tiles(REST), label), encoding="utf-8")
        subprocess.run(
            [CHROME, "--headless", "--disable-gpu", "--hide-scrollbars",
             "--force-device-scale-factor=2", "--window-size=1180,560",
             f"--screenshot={out}", f"file://{page}"],
            capture_output=True,
        )

    print(f"Wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
