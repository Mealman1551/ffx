# ffx Firefox Tarball Manager


ffx is a user space Firefox manager for Linux. It installs and manages multiple Firefox editions side by side using official Mozilla tarballs.

Each Firefox channel is fully isolated so multiple versions can exist at the same time.

## Features

*   Multiple Firefox channels side by side
*   No root required
*   Per channel executables
*   Per channel desktop entries
*   Switch versions without reinstalling
*   Clean uninstall support
*   Works on Debian, Fedora, Arch

## Supported channels

*   release
*   esr
*   beta
*   dev
*   nightly

## Installation

install by this command:


N/a

You will be prompted to choose channel and language.

## Commands

### Install Firefox

ffx install

Interactive install with channel and language selection.

### List installs

ffx list

Shows all installed versions and active selection.

### Use version

ffx use <channel>

ffx use dev

Switch active Firefox version.

### Remove version

ffx remove <channel>

ffx remove esr

Removes a Firefox installation.

## File locations

Install directory:

~/.local/opt/ffx/<channel>/

Binary links:

~/.local/bin/ffx-<channel>

Desktop entries:

~/.local/share/applications/ffx-<channel>.desktop

Config:

~/.config/ffx/config.json

## Example workflow

ffx install
ffx list
ffx use dev
ffx remove beta

### Notes


*   Each channel is fully isolated
*   No overwriting between installs
*   Switching does not reinstall Firefox
*   No root required
*   Updates require reinstall

### Future improvements

*   Automatic update checker
*   Rollback system
*   CLI autocomplete
*   Config presets
*   TUI interface