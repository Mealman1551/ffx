#!/usr/bin/env bash

set -e

INSTALL_DIR="$HOME/.local/bin"
TARGET="$INSTALL_DIR/ffx"
URL="https://raw.githubusercontent.com/Mealman1551/ffx/master/ffx.py"

mkdir -p "$INSTALL_DIR"

echo "Downloading ffx..."

wget -q -O "$TARGET" "$URL"

chmod +x "$TARGET"

echo "Installed ffx to $TARGET"

SHELL_RC=""

if [ -n "$BASH_VERSION" ]; then
    SHELL_RC="$HOME/.bashrc"
elif [ -n "$ZSH_VERSION" ]; then
    SHELL_RC="$HOME/.zshrc"
else
    SHELL_RC="$HOME/.profile"
fi

PATH_LINE='export PATH="$HOME/.local/bin:$PATH"'

if [ -f "$SHELL_RC" ]; then
    if ! grep -qF "$PATH_LINE" "$SHELL_RC"; then
        echo "" >> "$SHELL_RC"
        echo "$PATH_LINE" >> "$SHELL_RC"
        echo "Added PATH to $SHELL_RC"
    else
        echo "PATH already configured"
    fi
fi

echo ""
echo "Done. Restart your shell or run:"
echo "export PATH=\"$HOME/.local/bin:\$PATH\""