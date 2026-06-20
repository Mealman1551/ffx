#!/usr/bin/env bash

set -e

INSTALL_DIR="$HOME/.local/bin"
TARGET="$INSTALL_DIR/ffx"
URL="https://raw.githubusercontent.com/Mealman1551/ffx/master/ffx.py"

mkdir -p "$INSTALL_DIR"

echo "Downloading ffx..."

wget -qO "$TARGET.py" "$URL"

chmod +x "$TARGET.py"

cat > "$TARGET" << 'EOF'
#!/usr/bin/env bash
python3 "$HOME/.local/bin/ffx.py" "$@"
EOF

chmod +x "$TARGET"

echo "Installed ffx to $TARGET"