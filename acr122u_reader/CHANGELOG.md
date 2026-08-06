# Changelog

## 1.4.3

- Fix PC/SC state monitoring initialization.
- Establish the reader baseline with `SCARD_STATE_UNAWARE`.
- Feed the complete state returned by PC/SC into the next status-change call.
- Preserve pcsc-lite event-counter bits instead of manually reconstructing state.
- Add baseline state logging for removal-latency diagnostics.

## 1.4.2

- Replace APDU-based removal polling, which could block for roughly 30 seconds.
- Use PC/SC `SCardGetStatusChange` with a configurable millisecond timeout.
- Detect the reader's empty state without issuing a blocking card command.
- Keep the normal CardMonitor removal callback as a fallback.
- Continue suppressing duplicate removal events.

## 1.4.1

- Add fast active-card presence polling for near-immediate removal detection.
- Default removal polling interval is 150 ms.
- Keep the normal PC/SC removal callback as a fallback.
- Prevent duplicate card-removed events when both detection methods fire.
- Add configurable `removal_poll_interval`.

## 1.4.0

- Rebrand add-on and integration to **USB NFC Reader**.
- Keep ACR122U as the supported hardware model rather than the product name.


## 1.3.1

- Fix Home Assistant device trigger registration using the standard device-trigger schema.
- Add clear **NFC card scanned** and **NFC card removed** triggers.
- Add a native `Card activity` event entity.
- Include the card UID in event entity attributes.
- Keep card-present and tag sensors as status entities.

## 1.3.0

- Refactor the app into focused modules.
- Add structured startup diagnostics.
- Add HUN-001 and HUN-002 error codes.
- Detect missing ACR122U hardware.
- Detect when the reader is visible but cannot be opened.
- Create persistent notifications for likely Protection mode problems.
- Dismiss resolved reader notifications automatically.
- Improve startup log readability.
- Preserve native tags, entities, device triggers, and existing events.

## 1.2.1

- Notify users when a Home Assistant Core restart is required.
