#!/bin/bash
# MPDF File Type Registration for macOS
# Associates .mpdf files with Safari/default browser

set -e

# Create a minimal .app wrapper that opens .mpdf in the default browser
APP_DIR="$HOME/Applications/MPDF Viewer.app"
mkdir -p "$APP_DIR/Contents/MacOS"

# Create the launcher script
cat > "$APP_DIR/Contents/MacOS/mpdf-viewer" << 'SCRIPT'
#!/bin/bash
open -a Safari "$1" 2>/dev/null || open "$1"
SCRIPT
chmod +x "$APP_DIR/Contents/MacOS/mpdf-viewer"

# Create Info.plist with UTI registration
cat > "$APP_DIR/Contents/Info.plist" << 'PLIST'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleName</key>
    <string>MPDF Viewer</string>
    <key>CFBundleIdentifier</key>
    <string>com.mpdf.viewer</string>
    <key>CFBundleVersion</key>
    <string>1.0</string>
    <key>CFBundleExecutable</key>
    <string>mpdf-viewer</string>
    <key>CFBundleDocumentTypes</key>
    <array>
        <dict>
            <key>CFBundleTypeName</key>
            <string>MPDF Document</string>
            <key>CFBundleTypeExtensions</key>
            <array>
                <string>mpdf</string>
            </array>
            <key>CFBundleTypeRole</key>
            <string>Viewer</string>
            <key>LSHandlerRank</key>
            <string>Owner</string>
            <key>CFBundleTypeMIMETypes</key>
            <array>
                <string>application/mpdf</string>
            </array>
        </dict>
    </array>
    <key>UTImportedTypeDeclarations</key>
    <array>
        <dict>
            <key>UTTypeIdentifier</key>
            <string>com.mpdf.document</string>
            <key>UTTypeDescription</key>
            <string>MPDF Document</string>
            <key>UTTypeConformsTo</key>
            <array>
                <string>public.html</string>
            </array>
            <key>UTTypeTagSpecification</key>
            <dict>
                <key>public.filename-extension</key>
                <array>
                    <string>mpdf</string>
                </array>
                <key>public.mime-type</key>
                <string>application/mpdf</string>
            </dict>
        </dict>
    </array>
</dict>
</plist>
PLIST

# Register with Launch Services
/System/Library/Frameworks/CoreServices.framework/Frameworks/LaunchServices.framework/Support/lsregister -f "$APP_DIR" 2>/dev/null || true

echo "Done! MPDF Viewer installed to ~/Applications/"
echo "Double-click any .mpdf file to open it, or right-click > Open With > MPDF Viewer"
