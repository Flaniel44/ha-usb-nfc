# Changelog

## 1.3.1

- Fix Home Assistant device trigger registration using the standard device-trigger schema.
- Add clear **NFC card scanned** and **NFC card removed** triggers.
- Add an optional native Home Assistant Tag picker to both device triggers.
- Allow leaving the Tag field blank to trigger for any card.
- Filter scanned and removed events by the selected tag UID.
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
