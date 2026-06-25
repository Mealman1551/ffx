#!/usr/bin/env python3

import sys
import json
import tempfile
import urllib.request
import subprocess
from pathlib import Path
from datetime import datetime

BASE_URL = "https://download.mozilla.org/?product={product}&os=linux64&lang={lang}"

CHANNELS = {
    "release": "firefox-latest",
    "esr": "firefox-esr-latest",
    "beta": "firefox-beta-latest",
    "dev": "firefox-devedition-latest",
    "nightly": "firefox-nightly-latest"
}

DISPLAY_NAMES = {
    "release": "Firefox",
    "esr": "Firefox ESR",
    "beta": "Firefox Beta",
    "dev": "Firefox Developer Edition",
    "nightly": "Firefox Nightly"
}

LANGS = {
    "nl": "nl",
    "en": "en-US",
    "de": "de",
    "fr": "fr"
}

BASE_DIR = Path.home() / ".local" / "opt" / "ffx"
BIN_DIR = Path.home() / ".local" / "bin"
APPS_DIR = Path.home() / ".local" / "share" / "applications"
CONFIG_DIR = Path.home() / ".config" / "ffx"
CONFIG_FILE = CONFIG_DIR / "config.json"


def run(cmd):
    subprocess.run(cmd, check=True)


def load():
    if CONFIG_FILE.exists():
        return json.loads(CONFIG_FILE.read_text())
    return {"installs": {}}


def save(cfg):
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE.write_text(json.dumps(cfg, indent=2))


def download(url, out):
    urllib.request.urlretrieve(url, out)


def choose(options):
    try:
        keys = list(options.keys())

        for i, k in enumerate(keys, 1):
            print(f"[{i}] {k}")

        while True:
            raw = input("> ").strip()

            if not raw:
                print("Enter a number")
                continue

            try:
                idx = int(raw)
                if 1 <= idx <= len(keys):
                    return keys[idx - 1]
                print("Invalid choice")
            except ValueError:
                print("Enter a number")

    except (KeyboardInterrupt, EOFError):
        print("\nCancelled")
        sys.exit(0)


def install(cfg):
    print("Channel:")
    ch = choose(CHANNELS)

    print("Language:")
    lang = choose(LANGS)

    product = CHANNELS[ch]
    lang_code = LANGS[lang]

    url = BASE_URL.format(product=product, lang=lang_code)

    tmp = tempfile.mkdtemp()
    archive = Path(tmp) / "firefox.tar.xz"

    print("Downloading...")
    download(url, archive)

    install_path = BASE_DIR / ch

    if install_path.exists():
        run(["rm", "-rf", str(install_path)])

    install_path.mkdir(parents=True, exist_ok=True)

    print("Extracting...")
    run(["tar", "-xf", str(archive), "-C", str(install_path), "--strip-components=1"])

    firefox_bin = install_path / "firefox"

    if ch == "release":
        bin_name = "firefox"
        desktop_name = "firefox.desktop"
    else:
        bin_name = f"firefox-{ch}"
        desktop_name = f"firefox-{ch}.desktop"

    display_name = DISPLAY_NAMES[ch]

    bin_path = BIN_DIR / bin_name
    desktop_path = APPS_DIR / desktop_name

    BIN_DIR.mkdir(parents=True, exist_ok=True)
    APPS_DIR.mkdir(parents=True, exist_ok=True)

    if bin_path.exists() or bin_path.is_symlink():
        bin_path.unlink()

    bin_path.symlink_to(firefox_bin)

    icon_path = install_path / "browser" / "chrome" / "icons" / "default" / "default128.png"

    desktop_path.write_text(f"""[Desktop Entry]
Name={display_name}
Exec={bin_path} %u
Icon={icon_path}
Type=Application
Categories=Network;WebBrowser;
MimeType=text/html;text/xml;application/xhtml+xml;x-scheme-handler/http;x-scheme-handler/https;
StartupNotify=true
""")

    try:
        run(["update-desktop-database", str(APPS_DIR)])
    except Exception:
        pass

    cfg["installs"][ch] = {
        "lang": lang,
        "path": str(install_path),
        "bin": str(bin_path),
        "desktop": str(desktop_path)
    }

    save(cfg)

    print("Installed:", ch)


def list_installs(cfg):
    if not cfg["installs"]:
        print("No installs found")
        return

    for k, v in cfg["installs"].items():
        print(k, "-", v["lang"])


def remove(cfg, channel):
    if channel not in cfg["installs"]:
        print("Not found")
        return

    data = cfg["installs"][channel]

    path = Path(data["path"])
    bin_path = Path(data["bin"])
    desktop_path = Path(data["desktop"])

    if path.exists():
        run(["rm", "-rf", str(path)])

    if bin_path.exists() or bin_path.is_symlink():
        bin_path.unlink()

    if desktop_path.exists():
        desktop_path.unlink()

    legacy_bin = BIN_DIR / f"firefox-{channel}"
    legacy_desktop = APPS_DIR / f"firefox-{channel}.desktop"

    if legacy_bin.exists() or legacy_bin.is_symlink():
        legacy_bin.unlink()

    if legacy_desktop.exists():
        legacy_desktop.unlink()

    if channel == "release":
        if (BIN_DIR / "firefox").exists():
            (BIN_DIR / "firefox").unlink()

        if (APPS_DIR / "firefox.desktop").exists():
            (APPS_DIR / "firefox.desktop").unlink()

    try:
        run(["update-desktop-database", str(APPS_DIR)])
    except Exception:
        pass

    del cfg["installs"][channel]
    save(cfg)

    print("Removed:", channel)


def main():
    cfg = load()

    if len(sys.argv) < 2:
        print("ffx install | list | remove <channel>")
        return

    cmd = sys.argv[1]

    try:
        if cmd == "install":
            install(cfg)

        elif cmd == "list":
            list_installs(cfg)

        elif cmd == "remove":
            if len(sys.argv) < 3:
                print("Usage: ffx remove <channel>")
                return
            remove(cfg, sys.argv[2])

        else:
            print("Unknown command")

    except KeyboardInterrupt:
        print("\nInterrupted")
        sys.exit(0)


if __name__ == "__main__":
    main()