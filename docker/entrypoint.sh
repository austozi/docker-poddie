#!/bin/sh

set -eu

YTDLP_URL="https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp"
YTDLP_BIN="/tmp/yt-dlp"

echo "Updating yt-dlp..."

curl \
    --fail \
    --location \
    --silent \
    --show-error \
    --output "$YTDLP_BIN" \
    "$YTDLP_URL"

chmod 755 "$YTDLP_BIN"

echo "yt-dlp version:"
"$YTDLP_BIN" --version

export PATH="/tmp:$PATH"

python -m http.server \
    --bind 0.0.0.0 \
    8080 \
    --directory /data &
HTTP_PID=$!

cleanup() {
    kill "$HTTP_PID" 2>/dev/null || true
}

trap cleanup EXIT INT TERM

exec python -B -u -m poddie.main
