#!/bin/bash
# Double-click in Finder or run: ./preview.command
cd "$(dirname "$0")"

if ! command -v python3 >/dev/null 2>&1; then
  osascript -e 'display dialog "python3 not found. Install Python 3 from python.org or use: xcode-select --install" buttons {"OK"} default button "OK"'
  exit 1
fi

PORT="${PORT:-8765}"
echo "Starting server on http://127.0.0.1:${PORT}/"
echo "Edit index.html and refresh the browser. Press Ctrl+C here to stop."
echo ""

python3 -m http.server "$PORT" &
SERVER_PID=$!
sleep 1

if ! kill -0 "$SERVER_PID" 2>/dev/null; then
  echo "Server failed to start. Port $PORT may be in use. Try: PORT=8777 ./preview.command"
  exit 1
fi

open "http://127.0.0.1:${PORT}/"
wait "$SERVER_PID"
