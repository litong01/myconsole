#!/usr/bin/env python3
"""Rebuild preview/index.html from the current inject file.

The preview embeds Fully Kiosk's own launcher stylesheet and markup (copied from
https://www.fully-kiosk.com/samples/universal-launcher.html) so the desktop
render shows what the tablet will show.

The theme is added the same way FKB adds it - as HTML written into <head> at
runtime, which means a plain <script> tag in it does not execute. Keeping the
preview faithful to that is the point; the theme has to cope with it.

    python3 tools/make-preview.py            # as FKB injects it
    python3 tools/make-preview.py --no-js    # CSS only, to check the fallback
"""

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
INJECT = ROOT / "inject" / "launcher-inject.html"

FKB_HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>myconsole preview</title>

  <!-- Fully Kiosk's own launcher stylesheet, verbatim -->
  <style>
    * {margin:0; padding:0; }
    body {font-family: Arial, "Helvetica Neue", Helvetica, sans-serif; text-align:left; box-sizing:border-box; overflow-x:hidden; min-height:100%; }
    body {background-color: #FFFFFF;}
    body {font-size: 100%;}
    body {margin-top: 1em;}
    div.app, div.bookmark {margin:0.5em 1em 0.5em 1em; float:left; width:4em;height:6em;overflow-y:hidden;border: 0px solid #555;}
    div.appIcon img, div.bookmarkIcon img {width:4em;height:4em;}
    div.appName, div.bookmarkName {font-size:0.7em;line-height:1.25em;font-weight:bold;text-align:center;}
    div.app a, div.bookmark a {text-decoration:none;color:black;}
    p.error {margin:2em; font-size:2em; color:red; text-align: center;}
  </style>

  <style>
    .preview-banner {
      position: fixed;
      bottom: 0;
      left: 0;
      right: 0;
      z-index: 99;
      padding: 10px 16px;
      font: 12px/1.4 system-ui, sans-serif;
      color: #9aa0a6;
      background: rgba(0, 0, 0, 0.75);
      text-align: center;
    }
    .preview-banner code {
      color: #c4c7c5;
    }
  </style>

"""

ITEMS = [
    ("router", "my router"),
    ("switch", "my switch 109"),
    ("switch", "my switch 110"),
    ("streaming", "plex"),
    ("nas", "nas"),
    ("wifi", "upstairs ap"),
]


def body(note: str) -> str:
    tiles = []
    for index, (icon, label) in enumerate(ITEMS, start=1):
        tiles.append(
            f'  <div class="bookmark" id="b{index}">\n'
            f'    <a href="#">\n'
            f'      <div class="bookmarkIcon"><img src="../icons/png/{icon}.png" /></div>\n'
            f'      <div class="bookmarkName">{label}</div>\n'
            f"    </a>\n"
            f"  </div>\n"
        )
    return (
        "</head>\n<body>\n"
        "  <!-- Same shape FKB generates for each shortcut -->\n"
        + "".join(tiles)
        + f'\n  <p class="preview-banner">{note}</p>\n'
        "</body>\n</html>\n"
    )


def main() -> int:
    no_js = "--no-js" in sys.argv
    inject = INJECT.read_text(encoding="utf-8")

    # Drop the leading HTML comment; keep the <style> (and <script> unless --no-js).
    theme = inject.split("-->", 1)[1].lstrip()
    if no_js:
        theme = theme.split('<script id="myconsole-script">', 1)[0]

    note = (
        "Desktop preview, CSS only (script removed) — labels must still be readable."
        if no_js
        else "Desktop preview — theme injected exactly as Fully Kiosk injects it."
    )

    # A <template> keeps the theme inert until the injector writes it into <head>
    # as markup, matching how FKB applies it.
    injected = (
        '<template id="mc-theme">\n'
        + theme
        + "\n</template>\n"
        '<script>\n'
        '  document.head.insertAdjacentHTML(\n'
        '    "beforeend",\n'
        '    document.getElementById("mc-theme").innerHTML\n'
        '  );\n'
        "</script>\n"
    )

    out = ROOT / ("preview/index-nojs.html" if no_js else "preview/index.html")
    out.write_text(FKB_HEAD + injected + body(note), encoding="utf-8")
    print(f"Wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
