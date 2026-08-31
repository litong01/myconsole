# Fully Kiosk — recommended settings for myconsole

Use this as a checklist after unzipping **myconsole** and pasting `inject/launcher-inject.html`.

## Install the theme (required)

**Other Settings → Import Settings** → pick `fkb/myconsole-settings.json`.

That one import covers everything below in this section: the inject code, the
launcher as home screen, the hidden toolbars, and the back button. Only the keys
in the file change, so existing shortcuts and PINs are untouched.

Prefer to paste by hand? Use `inject/launcher-inject.txt` (Android will not open
the `.html` as text) into **Universal Launcher → Inject HTML Code in Launcher**,
then set the rest yourself:

| Setting | Recommended |
|---------|-------------|
| Show Launcher on Start | **ON** |
| Launcher Page Scaling | `100` (try `110` on large wall tablets) |
| Show Action Bar | OFF |
| Show Status Bar | OFF |
| Show Navigation Bar | OFF |
| Show Progress Bar | OFF |
| Enable Back Button | ON |

Launcher background and label colors come from the injected CSS, so the
**Launcher Background Color** and **Launcher Text Color** settings do not matter.

Home screen is then `fully://launcher` — add and remove shortcuts only via **Select Items to Show**.

## Universal Launcher

| Setting | Recommended |
|---------|-------------|
| Select Items to Show | Add your URLs and apps here |

## Device management (wall tablet)

| Setting | Recommended |
|---------|-------------|
| Keep Screen On | ON |
| Launch on Boot | ON |
| Screen Orientation | Landscape or Portrait (your choice) |

## Kiosk mode (optional, PLUS)

Shortcuts started from Universal Launcher are whitelisted automatically. Configure PIN, home button, and the rest as you normally would — myconsole does not change any of that.

## Per-shortcut name and icon

Set these per item in **Select Items to Show**, the same as without this theme:

- **Name** — shown under the tile, e.g. `my switch 109`
- **Icon** — use the file picker to choose from `myconsole/icons/`, e.g. `file:///sdcard/Download/myconsole/icons/switch.svg`

The theme never rewrites names or icons; it only lays the tiles out and styles them.

Bundled icons (`icons/`), all drawn to match:

| File | Use for |
|------|---------|
| `router.svg` | Routers, gateways |
| `switch.svg` | Network switches |
| `firewall.svg` | Firewalls |
| `wifi.svg` | Access points, Wi-Fi |
| `nas.svg` | NAS, storage |
| `server.svg` | Servers, hosts |
| `streaming.svg` | Streaming, media |
| `camera.svg` | Cameras, NVR |
| `dashboard.svg` | Dashboards, admin UIs |
| `default.svg` | Anything else |

Open `icons/gallery.html` in FKB or a browser to see them all with their paths. If an SVG will not load on your device, use `icons/png/<name>.png` instead.

## Verify

0. After importing, reload `fully://launcher` or restart FKB.
1. Open FKB → centered round tiles plus the clock.
2. Add a test URL with a name and icon in **Select Items to Show** → the tile appears with exactly that name and icon, no re-zipping.
3. Tap the tile → the site opens; Home (if enabled) → back to the launcher.
