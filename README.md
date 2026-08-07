# ha-usb-nfc

A Home Assistant OS app for the ACS ACR122U USB NFC reader, bundled with a
custom integration for native entities, Tags, and automation triggers.

Card placement and removal are sent to Home Assistant immediately. No MQTT,
HACS, or separate integration download is required.

## Requirements

- Home Assistant OS on an `aarch64` system
- ACS ACR122U PICC Interface (`072f:2200`)
- Protection mode disabled for the app

The app needs direct USB access because it runs `pcscd`, the CCID driver, and
PySCard inside its container.

## Installation

1. Open **Settings → Apps → App store** in Home Assistant.
2. Open the repository menu and add:

   `https://github.com/Flaniel44/ha-usb-nfc`

3. Install **USB NFC Reader**.
4. Disable **Protection mode** on the app's **Info** page.
5. Enable **Start on boot** and **Watchdog**, then start the app.
6. Restart Home Assistant Core when the app displays the restart-required
   notification. This loads the bundled custom integration.
7. Open **Settings → Devices & services → Add integration**, search for
   **USB NFC Reader**, and add it.

The Core restart is required after an update whenever the bundled integration
files change.

## Automation triggers

The recommended setup uses the reader's native device triggers:

```text
Settings → Automations & scenes
→ Create or edit an automation
→ Add trigger
→ Device
→ USB NFC Reader
→ NFC card scanned / NFC card removed
→ Optional Tag
```

- Leave **Tag** empty to trigger for every card.
- To create a card-specific trigger, scan the card once, name it under
  **Settings → Tags**, and select it in the trigger's **Tag** field.
- The card UID is available to the automation in the trigger event data.

The integration also exposes a **Card activity** event entity with `scanned`
and `removed` event types. It remains supported for existing automations and
for general event-entity triggers. Use the device trigger when you want the
cleanest card-specific setup in the automation UI.

## Entities

The **USB NFC Reader** device provides:

- **Card activity** — `scanned` and `removed` events with the card UID
- **Card present** — whether a card is currently on the reader
- **Current tag** — UID of the card currently present
- **Last tag** — UID of the most recently scanned card

Scanning an unknown card registers it with Home Assistant Tags automatically.

## Immediate card removal

Removal detection uses PC/SC reader-state notifications and normally reacts on
the first empty-state transition. The default maximum status-change wait is
150 ms. It does not repeatedly send UID commands, avoiding the long APDU timeout
some ACR122U and pcsc-lite combinations exhibit after removal.

The app logs separate timestamps for hardware detection and Home Assistant API
acceptance. These make it possible to distinguish reader latency from automation
execution latency.

### Options

```yaml
cooldown_seconds: 2
removal_poll_interval: 0.15
```

- `cooldown_seconds` suppresses duplicate scans of the same card.
- `removal_poll_interval` is the maximum PC/SC status wait in seconds. Values
  below `0.05` are clamped to `0.05`.

## Raw events

The original event-bus interface is preserved for existing and advanced
automations.

Card placed:

```yaml
event_type: acr122u_card_present
data:
  uid: C8149FEF
  reader: ACS ACR122U PICC Interface 00 00
```

Card removed:

```yaml
event_type: acr122u_card_removed
data:
  uid: C8149FEF
  reader: USB NFC Reader
```

These events are emitted by the app as soon as the corresponding reader state
is detected. The custom integration converts them into the device-attributed
triggers and Card activity events described above.

## Startup diagnostics

The app checks the Home Assistant API token, USB device, PC/SC reader access,
and bundled integration installation at startup. It creates persistent Home
Assistant notifications for common setup failures.

- `HUN-001`: The reader is detected but cannot be opened. Confirm that
  Protection mode is disabled, then restart the app.
- `HUN-002`: No supported USB reader is detected. Check the USB connection,
  then restart the app.

If a removal automation is delayed, compare these app log entries:

- `Card removed` — when PC/SC detected removal
- `Home Assistant accepted acr122u_card_removed` — when the event API call
  completed

After changing app versions, also confirm that Home Assistant Core was
restarted so the bundled integration version matches the app version.

## Supported hardware

Currently tested and supported:

- ACS ACR122U PICC Interface
- USB vendor ID `072f`
- USB product ID `2200`
- Home Assistant OS on Raspberry Pi (`aarch64`)

## License

MIT
