#!/usr/bin/env python3
"""Report the drawn bounds of each icon in icons/*.svg.

Sizes are compared as they are seen, so the numbers come from the rendered
geometry (via the browser's getBBox) rather than from reading path data. The
stroke straddles the geometry, so half the stroke width is added on each side.

    python3 tools/icon-bounds.py
"""

import json
import pathlib
import re
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
ICONS = ROOT / "icons"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

PAGE = """<!DOCTYPE html>
<meta charset="utf-8">
<body>
%s
<pre id="out"></pre>
<script>
  var out = {};
  var svgs = document.querySelectorAll("svg[data-name]");
  for (var i = 0; i < svgs.length; i++) {
    var svg = svgs[i];
    var box = svg.getBBox();
    var pen = parseFloat(svg.getAttribute("stroke-width") || "0");
    out[svg.dataset.name] = {
      x: +(box.x - pen / 2).toFixed(2),
      y: +(box.y - pen / 2).toFixed(2),
      w: +(box.width + pen).toFixed(2),
      h: +(box.height + pen).toFixed(2)
    };
  }
  document.getElementById("out").textContent = JSON.stringify(out);
</script>
"""


def measure(paths: list[pathlib.Path]) -> dict:
    blocks = []
    for path in paths:
        svg = path.read_text(encoding="utf-8")
        svg = svg.replace("<svg ", f'<svg data-name="{path.stem}" ', 1)
        blocks.append(svg)

    with tempfile.TemporaryDirectory() as tmp:
        page = pathlib.Path(tmp) / "bounds.html"
        page.write_text(PAGE % "\n".join(blocks), encoding="utf-8")
        dom = subprocess.run(
            [CHROME, "--headless", "--disable-gpu", "--dump-dom", f"file://{page}"],
            capture_output=True,
            text=True,
        ).stdout

    match = re.search(r'<pre id="out">(\{.*?\})</pre>', dom, re.S)
    if not match:
        print("could not read bounds from the rendered page", file=sys.stderr)
        raise SystemExit(1)
    return json.loads(match.group(1))


def main() -> int:
    paths = sorted(ICONS.glob("*.svg"))
    bounds = measure(paths)

    rows = []
    for name, box in bounds.items():
        # Geometric mean stands in for how large the symbol reads next to others.
        weight = (box["w"] * box["h"]) ** 0.5
        cx = box["x"] + box["w"] / 2
        cy = box["y"] + box["h"] / 2
        rows.append((weight, name, box, cx, cy))

    print(f"{'icon':<11}{'w':>7}{'h':>7}{'size':>8}{'center x':>10}{'center y':>10}")
    for weight, name, box, cx, cy in sorted(rows):
        print(
            f"{name:<11}{box['w']:>7.2f}{box['h']:>7.2f}{weight:>8.2f}"
            f"{cx:>10.2f}{cy:>10.2f}"
        )

    sizes = [r[0] for r in rows]
    print(f"\nsmallest {min(sizes):.2f}, largest {max(sizes):.2f} "
          f"({max(sizes) / min(sizes):.2f}x apart)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
