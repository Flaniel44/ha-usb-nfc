# Changelog

## 1.2.1

- Create a persistent Home Assistant notification when the bundled custom integration is installed or updated.
- The notification clearly tells the user that Home Assistant Core must be restarted.
- Retry notification delivery during boot until the Core API becomes available.
- Update project links for the `ha-usb-nfc` repository name.

## 1.2.0

- Bundle a Home Assistant custom integration in the app.
- Automatically install/update the integration under `custom_components/acr122u`.
- Register scanned UIDs as native Home Assistant Tags.
- Add a native ACR122U device.
- Add card-present, current-tag, and last-tag entities.
- Add UI device triggers for card placed and card removed.
- Retain custom events for backward compatibility.

## 1.1.0

- Emit card-present and card-removed events.
