# ha-usb-nfc

A Home Assistant OS app for reading NFC card UIDs from an ACS ACR122U USB reader.

The app runs `pcscd` inside its container, reads card UIDs through PC/SC, and sends local Home Assistant events when a card is placed on or removed from the reader.

## Events

Card placed:

```yaml
event_type: acr122u_card_present
data:
  uid: C8149FEF
  reader: ACR122U
```

Card removed:

```yaml
event_type: acr122u_card_removed
data:
  uid: C8149FEF
  reader: ACR122U
```

## Installation

1. In Home Assistant, open **Settings → Apps → App store**.
2. Open the repository menu and add:

   `https://github.com/Flaniel44/ha-usb-nfc`

3. Install **ACR122U NFC Reader**.
4. Disable **Protection mode**.
5. Enable **Start on boot** and **Watchdog**.
6. Start the app.

## Hardware

Tested with:

- ACS ACR122U PICC Interface
- USB vendor ID `072f`
- USB product ID `2200`
- Home Assistant OS on Raspberry Pi

## Important

Protection mode must be disabled so the app can open the USB smart-card reader.

This project is currently an app rather than a Core custom integration because direct USB access, `pcscd`, CCID libraries, and system packages are required.

## Native Home Assistant integration (v1.2.0)

The app bundles and installs a companion custom integration. After starting the
updated app, restart Home Assistant Core once and add **ACR122U NFC Reader**
under **Settings → Devices & services**.

This adds native Tags, entities, and device triggers without MQTT, HACS, or any
additional add-on.

## Startup diagnostics

The app performs a startup health check and creates persistent Home Assistant
notifications for common setup problems. Users do not need to inspect low-level
PC/SC or libusb errors to identify a missing reader or enabled Protection mode.

## Automation triggers

The ACR122U device provides two explicit device triggers:

- **NFC card scanned**
- **NFC card removed**

It also provides a **Card activity** event entity whose events contain the tag
UID. The Card present, Current tag, and Last tag entities remain available for
status and conditions.

## Fast removal detection

ha-usb-nfc actively polls the presented card at a configurable interval, so
**NFC card removed** automations react quickly instead of waiting for a delayed
PC/SC removal notification. The default interval is 150 ms.
