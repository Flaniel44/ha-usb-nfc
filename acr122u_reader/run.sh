#!/usr/bin/with-contenv bashio

set -e

echo "Starting PC/SC daemon..."
pcscd --foreground &

sleep 3

echo "Starting ha-usb-nfc..."
exec python3 -m app.main
