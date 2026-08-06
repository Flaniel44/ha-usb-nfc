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
