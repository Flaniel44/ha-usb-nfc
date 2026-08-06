#!/usr/bin/with-contenv bashio

set -e

echo "Starting PC/SC daemon..."
pcscd --foreground &

sleep 3

echo "Starting ACR122U reader service..."
exec python3 /reader.py
