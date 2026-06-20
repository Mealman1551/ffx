#!/usr/bin/env python3

import os
import sys
import json
import hashlib
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

LANGS = {
    "nl": "nl",
    "en": "en-US",
    "de": "de",
    "fr": "fr"
}

BASE_DIR = Path.home() / ".local" / "opt" / "ffx"
BIN_LINK = Path.home() / ".local" / "bin" / "firefox"
CONFIG_DIR = Path.home() / ".config" / "ffx"
CONFIG_FILE = CONFIG_DIR / "config.json"

def run(cmd):
    subprocess.run(cmd, check=True)

def load():
    if CONFIG_FILE.exists():
        return json.loads(CONFIG_FILE.read_text())
    return {"installs": {}, "active": None}

def save(cfg):
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE.write_text(json.dumps(cfg, indent=2))

def download(url, out):
    urllib.request.urlretrieve(url, out)

def choose(options):
    keys = list(options.keys())
    for i, k in enumerate(keys, 1):
        print(f"[{i}] {k}")
    return keys[int(input("> ")) - 1]

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

    version_id = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    install_path = BASE_DIR / version_id

    install_path.mkdir(parents=True, exist_ok=True)

    print("Extracting...")
    run(["tar", "-xf", str(archive), "-C", str(install_path), "--strip-components=1"])

    cfg["installs"][version_id] = {
        "channel": ch,
        "lang": lang,
        "path": str(install_path)
    }

    cfg["active"] = version_id

    activate(cfg, version_id)
    save(cfg)

    print("Installed:", version_id)

def activate(cfg, version_id):
    path = Path(cfg["installs"][version_id]["path"])
    target = path / "firefox"

    BIN_LINK.parent.mkdir(parents=True, exist_ok=True)

    if BIN_LINK.exists() or BIN_LINK.is_symlink():
        BIN_LINK.unlink()

    BIN_LINK.symlink_to(target)

    cfg["active"] = version_id
    save(cfg)

def list_installs(cfg):
    for k, v in cfg["installs"].items():
        active = "*" if cfg.get("active") == k else " "
        print(active, k, v["channel"], v["lang"])

def remove(cfg, version_id):
    if version_id not in cfg["installs"]:
        print("Not found")
        return

    path = Path(cfg["installs"][version_id]["path"])

    if path.exists():
        run(["rm", "-rf", str(path)])

    del cfg["installs"][version_id]

    if cfg.get("active") == version_id:
        cfg["active"] = None
        if cfg["installs"]:
            new_active = next(iter(cfg["installs"]))
            activate(cfg, new_active)

    save(cfg)

def update(cfg):
    print("Update check (simple re-install latest release)...")
    install(cfg)

def main():
    cfg = load()

    if len(sys.argv) < 2:
        print("ffx install|list|remove|activate|update")
        return

    cmd = sys.argv[1]

    if cmd == "install":
        install(cfg)

    elif cmd == "list":
        list_installs(cfg)

    elif cmd == "remove":
        remove(cfg, sys.argv[2])

    elif cmd == "activate":
        activate(cfg, sys.argv[2])

    elif cmd == "update":
        update(cfg)

    else:
        print("Unknown command")

if __name__ == "__main__":
    main()