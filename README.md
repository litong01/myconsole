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
/storage/emulated/0/Download/myconsole/
```

That is what Android's Downloads folder really is. File managers display it as
**Downloads**, the directory name on disk is `Download` (no `s`), and
`/sdcard/Download/myconsole/` is the same place by an older alias if FKB's picker
shows it that way. If you moved the folder elsewhere, substitute your path.

### 2. Install the theme by importing a settings file

Android usually refuses to open an `.html` file as text, so don't try to copy the
inject code by hand on the tablet. Import it instead:

**FKB → Settings → Other Settings → Import Settings** → pick

```
/storage/emulated/0/Download/myconsole/fkb/myconsole-settings.json
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
- **Icon** — one of the bundled icons below, e.g. `file:///storage/emulated/0/Download/myconsole/icons/switch.svg` (the icon field has a file picker, so you can browse to `myconsole/icons/` instead of typing)

The tile shows that name and that icon. New items appear automatically — no zip changes needed.

## The icon set

`icons/` holds ten icons drawn on one grid with the same stroke weight and accent colour, so a wall of tiles looks like a single product rather than a pile of favicons. Pick one in an item's **Icon** field:

| Icon | Use for | Path |
|------|---------|------|
| `router` | Routers, gateways | `file:///storage/emulated/0/Download/myconsole/icons/router.svg` |
| `switch` | Network switches | `file:///storage/emulated/0/Download/myconsole/icons/switch.svg` |
| `firewall` | Firewalls | `file:///storage/emulated/0/Download/myconsole/icons/firewall.svg` |
| `wifi` | Access points, Wi-Fi | `file:///storage/emulated/0/Download/myconsole/icons/wifi.svg` |
| `nas` | NAS, storage | `file:///storage/emulated/0/Download/myconsole/icons/nas.svg` |
| `server` | Servers, hosts | `file:///storage/emulated/0/Download/myconsole/icons/server.svg` |
| `streaming` | Streaming, media | `file:///storage/emulated/0/Download/myconsole/icons/streaming.svg` |
| `camera` | Cameras, NVR | `file:///storage/emulated/0/Download/myconsole/icons/camera.svg` |
| `dashboard` | Dashboards, admin UIs | `file:///storage/emulated/0/Download/myconsole/icons/dashboard.svg` |
| `default` | Anything else | `file:///storage/emulated/0/Download/myconsole/icons/default.svg` |

Adjust the paths if you moved the folder out of Downloads. Your own PNG/ICO/SVG files work the same way, and the icon field has a file picker so you can browse instead of typing.

Reuse one icon as often as you like — `my switch 109`, `my switch 110`, and `my switch 111` can all point at `switch.svg`, and only the names differ on screen.

**See them first:** open `icons/gallery.html` (on your computer or the tablet) for the whole set rendered in the same round tile as the console, each with its path.

**PNG fallback:** if FKB will not accept an SVG on your device, use the matching 256px PNG:

```
file:///storage/emulated/0/Download/myconsole/icons/png/switch.png
```

After editing an SVG, re-render the PNGs with `tools/make-png.sh` (needs Chrome on your computer, not on the tablet).

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
  tools/make-settings.py        ← rebuild the importable settings file
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
