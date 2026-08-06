#!/usr/bin/with-contenv bashio

set -e

INTEGRATION_SOURCE="/opt/acr122u_integration"
INTEGRATION_TARGET="/homeassistant/custom_components/acr122u"
RESTART_FLAG="/data/home_assistant_restart_required"

mkdir -p "/homeassistant/custom_components"

if [ ! -d "${INTEGRATION_TARGET}" ] || ! diff -qr "${INTEGRATION_SOURCE}" "${INTEGRATION_TARGET}" >/dev/null 2>&1; then
    echo "Installing/updating the bundled ACR122U custom integration..."
    rm -rf "${INTEGRATION_TARGET}"
    cp -R "${INTEGRATION_SOURCE}" "${INTEGRATION_TARGET}"
    touch "${RESTART_FLAG}"
    echo "Home Assistant Core restart required. A persistent notification will be created."
fi

echo "Starting PC/SC daemon..."
pcscd --foreground &

sleep 3

echo "Starting ACR122U reader service..."
exec python3 /reader.py
