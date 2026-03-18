#!/bin/bash
# MPDF File Type Registration for Linux
# Registers .mpdf files to open in the default browser

set -e

DESKTOP_DIR="$HOME/.local/share/applications"
MIME_DIR="$HOME/.local/share/mime/packages"

mkdir -p "$DESKTOP_DIR" "$MIME_DIR"

# Create MIME type definition
cat > "$MIME_DIR/mpdf.xml" << 'MIMEEOF'
<?xml version="1.0" encoding="UTF-8"?>
<mime-info xmlns="http://www.freedesktop.org/standards/shared-mime-info">
  <mime-type type="application/mpdf">
    <comment>MPDF Document</comment>
    <glob pattern="*.mpdf"/>
    <sub-class-of type="text/html"/>
  </mime-type>
</mime-info>
MIMEEOF

# Create .desktop entry
cat > "$DESKTOP_DIR/mpdf-viewer.desktop" << 'DESKTOPEOF'
[Desktop Entry]
Type=Application
Name=MPDF Viewer
Comment=Open MPDF documents in the browser
Exec=xdg-open %f
MimeType=application/mpdf;
NoDisplay=true
DESKTOPEOF

# Update MIME database
update-mime-database "$HOME/.local/share/mime" 2>/dev/null || true

# Set default application
xdg-mime default mpdf-viewer.desktop application/mpdf 2>/dev/null || true

echo "Done! .mpdf files are now associated with your default browser."
echo "Try: xdg-open test.mpdf"
