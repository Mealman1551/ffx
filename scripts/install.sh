#!/usr/bin/env bash

set -e

INSTALL_DIR="$HOME/.local/bin"
TARGET="$INSTALL_DIR/ffx"
PY_TARGET="$INSTALL_DIR/ffx.py"
URL="https://raw.githubusercontent.com/Mealman1551/ffx/master/ffx.py"

mkdir -p "$INSTALL_DIR"

echo "Downloading ffx..."

wget -qO "$PY_TARGET" "$URL"

chmod +x "$PY_TARGET"

cat > "$TARGET" << EOF
#!/usr/bin/env bash
exec python3 "$PY_TARGET" "\$@"
EOF

chmod +x "$TARGET"

# PATH fix (BELANGRIJK)
if ! echo "$PATH" | grep -q "$HOME/.local/bin"; then
    echo ""
    echo "WARNING: ~/.local/bin is not in PATH"
    echo "Add this to your shell config:"
    echo 'export PATH="$HOME/.local/bin:$PATH"'
fi

echo "Installed ffx to $TARGET"
echo "Run: ffx"