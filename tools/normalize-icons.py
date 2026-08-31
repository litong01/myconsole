#!/usr/bin/env python3
"""Give every icon in icons/*.svg the same visual size and center.

Each symbol keeps its own drawing; only its scale and position on the 24x24 grid
change. A symbol reads as "big" next to another based on the area it covers, so
sizes are matched on the geometric mean of the drawn box rather than on width or
height alone - a wide flat switch stays wider and shorter than a tall shield,
but neither dominates the row.

Artwork is wrapped in a <g> that carries the transform and a compensating
stroke-width, so the stroke lands at the same weight in every icon no matter how
much that icon was scaled. Running this twice is safe; the wrapper is rebuilt.

    python3 tools/normalize-icons.py            # rewrite the SVGs
    python3 tools/normalize-icons.py --dry-run  # just report

Regenerate the PNGs afterwards with tools/make-png.sh.
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

# Target size and the box nothing may exceed, in grid units. The caps keep wide
# symbols from spilling toward the edge of the circular well.
TARGET = 16.0
MAX_W = 19.5
MAX_H = 18.5
CENTER = 12.0
PEN = 1.5

WRAPPER = re.compile(r'\n?\s*<g id="mc-fit"[^>]*>(.*?)\n?\s*</g>\s*(?=</svg>)', re.S)

PAGE = """<!DOCTYPE html>
<meta charset="utf-8">
<body>
%s
<pre id="out"></pre>
<script>
  var out = {};
  var svgs = document.querySelectorAll("svg[data-name]");
  for (var i = 0; i < svgs.length; i++) {
    var box = svgs[i].getBBox();
    out[svgs[i].dataset.name] = {
      x: +box.x.toFixed(4), y: +box.y.toFixed(4),
      w: +box.width.toFixed(4), h: +box.height.toFixed(4)
    };
  }
  document.getElementById("out").textContent = JSON.stringify(out);
</script>
"""


def unwrap(svg: str) -> str:
    """Drop a previous run's wrapper so measurements are of the raw artwork."""
    match = WRAPPER.search(svg)
    if not match:
        return svg
    body = re.sub(r"^\n", "", match.group(1))
    body = re.sub(r"^ {2}", "", body, flags=re.M)
    return svg[: match.start()] + "\n" + body + "\n" + svg[match.end():]


def measure(sources: dict) -> dict:
    """Geometry bounds, excluding the stroke, as the browser lays them out."""
    blocks = [
        svg.replace("<svg ", f'<svg data-name="{name}" ', 1)
        for name, svg in sources.items()
    ]
    with tempfile.TemporaryDirectory() as tmp:
        page = pathlib.Path(tmp) / "bounds.html"
        page.write_text(PAGE % "\n".join(blocks), encoding="utf-8")
        dom = subprocess.run(
            [CHROME, "--headless", "--disable-gpu", "--dump-dom", f"file://{page}"],
            capture_output=True, text=True,
        ).stdout

    match = re.search(r'<pre id="out">(\{.*?\})</pre>', dom, re.S)
    if not match:
        print("could not read bounds from the rendered page", file=sys.stderr)
        raise SystemExit(1)
    return json.loads(match.group(1))


def visual(gw: float, gh: float, scale: float) -> tuple[float, float]:
    """Drawn box at a given scale: geometry scales, the stroke does not."""
    return gw * scale + PEN, gh * scale + PEN


def fit(gw: float, gh: float) -> float:
    lo, hi = 0.2, 3.0
    for _ in range(60):
        mid = (lo + hi) / 2
        w, h = visual(gw, gh, mid)
        if (w * h) ** 0.5 < TARGET:
            lo = mid
        else:
            hi = mid
    scale = (lo + hi) / 2

    # Never let the caps be exceeded, even at the cost of the target size.
    return min(scale, (MAX_W - PEN) / gw, (MAX_H - PEN) / gh)


def main() -> int:
    dry_run = "--dry-run" in sys.argv
    paths = sorted(ICONS.glob("*.svg"))

    sources = {p.stem: unwrap(p.read_text(encoding="utf-8")) for p in paths}
    bounds = measure(sources)

    print(f"{'icon':<11}{'scale':>7}{'size':>17}{'box':>18}")
    for path in paths:
        name = path.stem
        box = bounds[name]
        scale = fit(box["w"], box["h"])
        w, h = visual(box["w"], box["h"], scale)

        before = ((box["w"] + PEN) * (box["h"] + PEN)) ** 0.5
        after = (w * h) ** 0.5

        # translate() is applied before scale(), so offsets are in scaled units.
        tx = CENTER - scale * (box["x"] + box["w"] / 2)
        ty = CENTER - scale * (box["y"] + box["h"] / 2)

        print(f"{name:<11}{scale:>7.3f}"
              f"{before:>8.2f} -> {after:<6.2f}"
              f"{w:>9.2f} x {h:<6.2f}")

        if dry_run:
            continue

        svg = sources[name]
        body = svg.split(">", 1)[1].rsplit("</svg>", 1)[0].strip("\n")
        body = re.sub(r"^", "  ", body, flags=re.M)
        head = svg.split(">", 1)[0] + ">"

        path.write_text(
            f"{head}\n"
            f'  <g id="mc-fit" stroke-width="{PEN / scale:.4f}"'
            f' transform="translate({tx:.4f} {ty:.4f}) scale({scale:.4f})">\n'
            f"{body}\n"
            f"  </g>\n"
            f"</svg>\n",
            encoding="utf-8",
        )

    if dry_run:
        print("\ndry run, nothing written")
    else:
        print(f"\nrewrote {len(paths)} icons; now run tools/make-png.sh")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
