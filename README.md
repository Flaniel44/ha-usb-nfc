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

### Non-blocking card removal

Removal detection uses PC/SC reader-state changes rather than repeatedly sending
commands to a card that may already be absent. This avoids the approximately
30-second command timeout seen with some ACR122U configurations.

### Synchronized PC/SC state monitoring

Removal monitoring first establishes the reader's complete PC/SC state and then
tracks changes from that baseline. This avoids falling back to the reader's
slower removal callback when additional state flags are present.

### Instrumented removal timing

The app releases the UID-reading PC/SC connection before monitoring for card
removal. Timestamped logs show when removal was detected and how many
milliseconds Home Assistant took to accept the event, making latency problems
easier to isolate.

## Recommended automation path

Use the native reader device triggers:

```text
Add trigger
→ Device
→ USB NFC Reader
→ NFC card scanned / NFC card removed
→ Optional named Tag
```

The integration attributes each trigger to the specific reader device and
supports selecting tags already registered under **Settings → Tags**. The
legacy Card activity event entity is no longer loaded for new installations.

### Native trigger discovery

Version 1.4.6 aligns device-trigger registration with Home Assistant's official
device automation scaffold. After restarting Home Assistant Core, the reader
device exposes **NFC card scanned** and **NFC card removed**, with an optional
Home Assistant Tag selector.

The optional **Tag** field makes either device trigger card-specific. Scan an
unknown card once to register it under **Settings → Tags**, give it a friendly
name, then select that tag while configuring the trigger. Leave **Tag** empty
to react to every card.
