# myconsole — Nest-style theme for Fully Kiosk Browser

A zip-ready package that restyles the **Fully Kiosk Browser (FKB) Universal Launcher** into a clean, centered, Google Nest–inspired home console. You keep adding and removing shortcuts the normal FKB way.

## What this does

- Keeps FKB's **Universal Launcher** as the home screen.
- Injects CSS so tiles are **centered**, **round**, and **dark/minimal**, with the count of shortcuts driving the grid.
- Adds a large clock and date above the tiles.
- Ships optional SVG icons you can point FKB at (router, switch, streaming, NAS, firewall, Wi-Fi AP).

## What this does not do

- Does not replace FKB or its settings UI.
- Does not keep its own list of URLs.
- Does not touch shortcut **names** or **icons** — whatever you set in FKB is what shows.

## Quick setup

### 1. Get the zip onto the tablet

Each push to `main` publishes **myconsole.zip** at:

https://github.com/litong01/myconsole/releases/latest

1. On the tablet, download **myconsole.zip** from that page (or from the **Actions** run artifact).
2. Unzip it where it landed — the Downloads folder — so you end up with a `myconsole` folder there containing `inject/`, `icons/`, `fkb/`, and `README.md`.

Every path in this README then starts with:

```
/sdcard/Download/myconsole/
```

`/sdcard` is Android's shorthand for internal storage, and it is the form Fully
Kiosk's own docs use for `file://` paths. File managers show the folder as
**Downloads** while the directory on disk is `Download`, no `s`. If a picker
prints the longer `/storage/emulated/0/Download/myconsole/`, that is the same
place. If you moved the folder, substitute your path.

### 2. Install the theme by importing a settings file

Android usually refuses to open an `.html` file as text, so don't try to copy the
inject code by hand on the tablet. Import it instead:

**FKB → Settings → Other Settings → Import Settings** → pick

```
/sdcard/Download/myconsole/fkb/myconsole-settings.json
```

Only the keys in that file are applied, so your existing shortcuts, PIN, and
other settings are left alone. It sets:

| Key | Effect |
|-----|--------|
| `launcherInjectCode` | The whole theme (CSS + clock + centering) |
| `showAppLauncherOnStart` | Universal Launcher becomes the home screen |
| `showActionBar`, `showStatusBar`, `showNavigationBar`, `showProgressBar` | Off, for a clean console |
| `enableBackButton` | Back returns from a device page to the launcher |

Then reload with `fully://launcher` (or restart FKB) and you should see the dark
centered console.

**Manual fallback:** if you would rather paste it, use
`inject/launcher-inject.txt` — same content, but the `.txt` extension opens in
any Android text editor. Paste it into **Settings → Universal Launcher → Inject
HTML Code in Launcher**.

### 3. FKB — device options (optional)

| Setting | Value |
|--------|--------|
| **Keep Screen On** | ON (Device Management) |
| **Launch on Boot** | ON |
| **Screen Orientation** | however the tablet is mounted |

See `fkb/recommended-settings.md` for the full checklist.

### 4. Add your shortcuts (normal FKB flow)

**Settings → Universal Launcher → Select Items to Show**

For each item you set, exactly as you would without this theme:

- **URL** — e.g. `http://192.168.1.109` or `http://plex.local:32400/web`
- **Name** — e.g. `my switch 109`
- **Icon** — one of the bundled PNGs below, e.g. `file:///sdcard/Download/myconsole/icons/png/switch.png` (the icon field has a file picker, so you can browse to `myconsole/icons/png/` instead of typing)

The tile shows that name and that icon. New items appear automatically — no zip changes needed.

## The icon set

Icons drawn on one grid with the same stroke weight and accent colour, so a wall of tiles looks like a single product rather than a pile of favicons.

**Use the PNGs in `icons/png/`.** FKB decodes a shortcut icon into a bitmap rather than rendering it in the WebView, so it will not accept the `.svg` files. The SVGs in `icons/` are the editable sources for the PNGs.

| Use for | Icon path |
|---------|-----------|
| Routers, gateways | `file:///sdcard/Download/myconsole/icons/png/router.png` |
| Network switches | `file:///sdcard/Download/myconsole/icons/png/switch.png` |
| Power switches | `file:///sdcard/Download/myconsole/icons/png/power.png` |
| Firewalls | `file:///sdcard/Download/myconsole/icons/png/firewall.png` |
| Access points, Wi-Fi | `file:///sdcard/Download/myconsole/icons/png/wifi.png` |
| NAS, storage | `file:///sdcard/Download/myconsole/icons/png/nas.png` |
| Servers, hosts | `file:///sdcard/Download/myconsole/icons/png/server.png` |
| Streaming, media | `file:///sdcard/Download/myconsole/icons/png/streaming.png` |
| Cameras, NVR | `file:///sdcard/Download/myconsole/icons/png/camera.png` |
| Dashboards, admin UIs | `file:///sdcard/Download/myconsole/icons/png/dashboard.png` |
| Anything else | `file:///sdcard/Download/myconsole/icons/png/default.png` |

Adjust the paths if you moved the folder out of Downloads. Your own PNG or ICO files work the same way, and the icon field has a file picker so you can browse instead of typing.

Reuse one icon as often as you like — `my switch 109`, `my switch 110`, and `my switch 111` can all point at `switch.png`, and only the names differ on screen.

**See them first:** open `icons/gallery.html` (on your computer or the tablet) for the whole set rendered in the same round tile as the console, each with the exact path to paste.

Every symbol is scaled to the same visual size and centered on the same grid, so
a monitor and a flat switch take up equal room side by side and no single tile
looks oversized in a row — only the drawing inside each circle differs.

The PNGs are 256px with a transparent background. After editing an SVG, run
`tools/normalize-icons.py` to bring it back in line with the rest, then
`tools/make-png.sh` to re-render (both need Chrome on your computer, not on the
tablet). `tools/icon-bounds.py` reports what each icon currently measures, and
`tools/icon-sheet.py` renders the whole set in tiles for comparison.

## Preview on desktop

Open `preview/index.html` in a browser to see the layout with sample tiles (no FKB required).

## File layout

```
myconsole/
  fkb/myconsole-settings.json   ← import this in FKB (installs the theme)
  inject/launcher-inject.html   ← source of the theme
  inject/launcher-inject.txt    ← same, for manual paste on Android
  icons/*.svg                   ← icons to point FKB at
  icons/png/*.png               ← same icons as 256px PNG
  icons/gallery.html            ← browse the set, copy paths
  preview/index.html            ← desktop preview of the console
  fkb/recommended-settings.md
  tools/make-png.sh             ← re-render PNGs after editing an SVG
  tools/normalize-icons.py      ← match icon sizes after editing an SVG
  tools/icon-bounds.py          ← report what each icon measures
  tools/icon-sheet.py           ← render the set side by side
  tools/make-settings.py        ← rebuild the importable settings file
  tools/make-preview.py         ← rebuild the desktop preview
  tools/package.sh              ← build the tablet zip
```

`fkb/myconsole-settings.json` and `inject/launcher-inject.txt` are generated at
package time, so they only exist in the zip — never edited by hand.

## Troubleshooting

- **Tiles not centered / look unchanged** — Confirm **Inject HTML Code in Launcher** is saved and **Show Launcher on Start** is ON, then reload `fully://launcher`.
- **Icon shows as broken** — Check the file path in the item's icon field and that the file exists after unzip.
- **Tiles too big or too small** — Change `--mc-tile` near the top of the inject file, or use FKB's **Launcher Page Scaling**.
- **Different launcher markup** — The theme targets `#list` / `.item`. If your FKB build differs, enable WebView debugging and check the class names.

## License

Use and modify freely for personal / internal use.
