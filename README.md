# Home Assistant ACR122U

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

   `https://github.com/Flaniel44/home-assistant-acr122u`

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
