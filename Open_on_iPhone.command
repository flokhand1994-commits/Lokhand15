#!/bin/bash
# Double-click this file (in Finder) to share flashcards on your Wi-Fi.
# Then scan the QR code with your iPhone Camera, or open the URL shown.

cd "$(dirname "$0")"
PORT=8765
IP=$(ipconfig getifaddr en0 2>/dev/null || ipconfig getifaddr en1 2>/dev/null || echo "")
if [ -z "$IP" ]; then
  IP="YOUR_MAC_IP"
fi

URL="http://${IP}:${PORT}/"

clear
echo ""
echo "  ════════════════════════════════════════════════════════════"
echo "   Dutch flashcards — iPhone (same Wi-Fi as this Mac)"
echo "  ════════════════════════════════════════════════════════════"
echo ""
echo "   1. Open this address on your iPhone in Safari:"
echo ""
echo "      $URL"
echo ""
echo "   2. Or scan the QR code in the page that opens on this Mac."
echo ""
echo "   URL copied to clipboard — paste in Messages / Notes if needed."
echo ""
echo "   Press Ctrl+C in this window to stop the server."
echo "  ════════════════════════════════════════════════════════════"
echo ""

echo -n "$URL" | pbcopy

python3 -m http.server "$PORT" --bind 0.0.0.0 &
SERVER_PID=$!
sleep 0.8
open "$URL" 2>/dev/null || true
wait $SERVER_PID
