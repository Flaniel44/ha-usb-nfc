#!/usr/bin/with-contenv bashio

set -e

INTEGRATION_SOURCE="/opt/acr122u_integration"
INTEGRATION_TARGET="/homeassistant/custom_components/acr122u"

mkdir -p "/homeassistant/custom_components"
if [ ! -d "${INTEGRATION_TARGET}" ] || ! diff -qr "${INTEGRATION_SOURCE}" "${INTEGRATION_TARGET}" >/dev/null 2>&1; then
    echo "Installing/updating the bundled ACR122U custom integration..."
    rm -rf "${INTEGRATION_TARGET}"
    cp -R "${INTEGRATION_SOURCE}" "${INTEGRATION_TARGET}"
    echo "ACR122U integration installed. Restart Home Assistant Core if this is the first install or an integration update."
fi

echo "Starting PC/SC daemon..."
pcscd --foreground &

sleep 3

echo "Starting ACR122U reader service..."
exec python3 /reader.py
