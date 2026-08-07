# ACR122U NFC Reader

## First-time setup after installing version 1.2.0

1. Disable Protection mode.
2. Start the app.
3. Restart Home Assistant Core once.
4. Go to **Settings → Devices & services → Add integration**.
5. Search for **ACR122U NFC Reader** and add it.

The app installs the bundled custom integration into Home Assistant automatically.

## Native features

- Unknown cards automatically appear under **Settings → Tags** after the first scan.
- Device triggers: **Card placed** and **Card removed**.
- Entities:
  - Card present
  - Current tag
  - Last tag

The existing events remain available:

- `acr122u_card_present`
- `acr122u_card_removed`

## Startup diagnostics

Version 1.3.0 checks:

- Home Assistant API token availability
- USB reader detection
- PC/SC reader access
- Bundled integration status

Common error codes:

- `HUN-001`: Reader detected but cannot be opened. Protection mode is likely enabled.
- `HUN-002`: Supported USB reader not detected.

## Clear automation triggers

After updating the app, restart Home Assistant Core so the updated integration
files load.

In the automation editor:

1. Add a trigger.
2. Choose **Device**.
3. Select **ACR122U NFC Reader**.
4. Select either:
   - **NFC card scanned**
   - **NFC card removed**

The device also exposes a **Card activity** event entity with `scanned` and
`removed` event types. The event includes the scanned card's `uid`.

## Fast card-removal detection

Version 1.4.1 actively checks the currently presented card rather than relying
only on the slower PC/SC removal callback.

The default interval is:

```yaml
removal_poll_interval: 0.15
```

This means card removal is normally detected within roughly 150–300 ms. Lower
values respond faster but create more USB traffic. Values below 0.05 seconds are
automatically clamped to 0.05 seconds.

## Non-blocking removal monitoring

Version 1.4.2 no longer sends repeated UID commands to determine whether the
card is still present. Some ACR122U/PCSC combinations can block those commands
for approximately 30 seconds after removal.

The app now uses PC/SC reader-state monitoring with the configured
`removal_poll_interval` as its maximum wait time. The default remains 150 ms.

## Reader-state synchronization

Version 1.4.3 initializes PC/SC monitoring with `SCARD_STATE_UNAWARE`, obtains
the reader's full baseline state, and passes each returned state directly into
the following status-change call. This matches PySCard's documented monitoring
pattern and prevents the fast watcher from remaining out of sync while the
slower CardMonitor callback eventually reports removal.

## Instrumented removal diagnostics

Version 1.4.4 explicitly releases the temporary PC/SC connection immediately
after reading a card UID. Removal monitoring begins only after that handle has
been closed.

Logs now include millisecond timestamps and report how long Home Assistant took
to accept each event. This separates:

- reader/PCSC removal-detection latency;
- add-on-to-Home-Assistant API latency;
- automation execution latency.

## Native device triggers

Version 1.4.5 makes the intended automation path explicit:

1. Open **Settings → Automations & scenes**.
2. Add a trigger.
3. Choose **Device**.
4. Select **USB NFC Reader**.
5. Choose **NFC card scanned** or **NFC card removed**.
6. Optionally select a named tag from **Settings → Tags**.

The previous `Card activity` event entity is no longer loaded for new
installations. Existing raw events remain available for backward compatibility.

## Device-trigger discovery fix

Version 1.4.6 follows Home Assistant's device-trigger scaffold:

- `TRIGGER_SCHEMA` extends `homeassistant.helpers.device_automation.TRIGGER_BASE_SCHEMA`;
- Home Assistant Core applies the trigger schema automatically;
- the delegated event configuration is validated with the event trigger schema.

After updating, restart Home Assistant Core and create the automation through:

**Add trigger → Device → USB NFC Reader → NFC card removed**

## Experimental integration triggers

Version 1.5.0 adds Home Assistant's newer integration-provided trigger platform.

In the automation editor, search for:

- **USB NFC Reader: NFC card scanned**
- **USB NFC Reader: NFC card removed**

Choose the reader device and optionally select a named Home Assistant Tag.

Home Assistant currently labels this API as actively developing, so the
implementation may require updates after future Home Assistant releases.
