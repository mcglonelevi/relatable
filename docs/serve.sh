#!/bin/sh
# Serve the site at http://localhost:8000 (pass a port to change it: ./serve.sh 3000).
# The pages use absolute paths (/assets/...), so they need a server; opening the .html files directly won't load styles.
cd "$(dirname "$0")" || exit 1
PORT="${1:-8000}"
echo "Chaotick site running at http://localhost:$PORT  (Ctrl+C to stop)"
exec python3 -m http.server "$PORT" --bind 127.0.0.1
