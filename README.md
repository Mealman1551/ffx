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

```bash
wget -qO- https://raw.githubusercontent.com/Mealman1551/ffx/master/scripts/install.sh | bash
```

You will be prompted to choose channel and language.

## Commands

### Install Firefox

```bash
ffx install
```

This will list all available channels
Use the number you want to install

### List installs

```bash
ffx list
```

Shows all installed versions their "IDs", example `dev - nl`


### Remove version

```bash
ffx remove <channel/id>
```

Removes a Firefox installation.

## File locations

Install directory:

`~/.local/opt/ffx/<channel>/`

Binary links:

`~/.local/bin/ffx-<channel>`

Desktop entries:

`~/.local/share/applications/ffx-<channel>.desktop`

Config:

`~/.config/ffx/config.json`

## Example workflow

`ffx install`
`ffx list`
`ffx remove <channel>`

### Notes


*   Each channel is fully isolated
*   No overwriting between installs
*   Switching does not reinstall Firefox
*   No root required
*   Updates require reinstall

--

## License

This project is licensed under GPLv3

--
Made with 💚 by Mealman1551

###### &copy 2026 - Mealman1551 