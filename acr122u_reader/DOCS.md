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

### Selecting a specific tag

After choosing **NFC card scanned** or **NFC card removed**, an optional **Tag**
field is displayed. It uses Home Assistant's native tag selector and lists tags
registered under **Settings → Tags**.

- Select a named tag to trigger only for that card.
- Leave the field blank to trigger for any card.
- A new card must be scanned once before it appears in the Tags list.
