#!/usr/bin/env python3
"""Build an FKB settings file that carries the theme.

Fully Kiosk's Other Settings -> Import Settings applies only the keys present
in the file, so this holds the inject code plus the few toggles the theme needs.
Colors and label styling are handled by the injected CSS, not by settings keys.
"""

import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
INJECT = ROOT / "inject" / "launcher-inject.html"


def build(inject_code: str) -> dict:
    return {
        "launcherInjectCode": inject_code,
        "showAppLauncherOnStart": True,
        "showActionBar": False,
        "showStatusBar": False,
        "showNavigationBar": False,
        "showProgressBar": False,
        "enableBackButton": True,
    }


def main() -> int:
    if not INJECT.is_file():
        print(f"missing {INJECT}", file=sys.stderr)
        return 1

    out_path = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "dist" / "myconsole-settings.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    settings = build(INJECT.read_text(encoding="utf-8"))
    out_path.write_text(json.dumps(settings, indent=2) + "\n", encoding="utf-8")

    # Fail loudly here rather than on the tablet, where a bad file just gets ignored.
    reloaded = json.loads(out_path.read_text(encoding="utf-8"))
    assert reloaded["launcherInjectCode"] == settings["launcherInjectCode"]
    assert "myconsole-stage" in reloaded["launcherInjectCode"]

    print(f"Wrote {out_path} ({out_path.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
