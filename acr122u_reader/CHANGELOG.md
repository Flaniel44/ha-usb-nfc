# Changelog

## 1.5.0

- Add experimental integration-provided automation triggers using `trigger.py`.
- Add `triggers.yaml` descriptions for **NFC card scanned** and **NFC card removed**.
- Add native reader device targeting.
- Add an optional Home Assistant Tag selector.
- Attach directly to the normalized `acr122u_event` event.
- Disable the generic Card Present binary sensor by default for new installations.
- Preserve raw and legacy device triggers for backward compatibility.
- Declare the custom integration as an integration type of `device`.

> Note: Home Assistant currently marks the integration trigger API as actively
> developing and subject to change without deprecation.

## 1.4.6

- Fix native device-trigger discovery using Home Assistant's documented `TRIGGER_BASE_SCHEMA`.
- Stop manually applying `TRIGGER_SCHEMA`; Home Assistant Core now applies it.
- Validate delegated event triggers with Home Assistant's `event_trigger.TRIGGER_SCHEMA`.
- Preserve the optional native Tag selector.
- Mark Card Present as a diagnostic entity so generic occupancy triggers are de-emphasized.
- Preserve the corrected modular GitHub Actions validation workflow.

## 1.4.5

- Make **NFC card scanned** and **NFC card removed** the primary automation UI triggers.
- Normalize reader activity into a device-attributed `acr122u_event`.
- Filter device triggers by the actual Home Assistant reader `device_id`.
- Keep the optional native Home Assistant Tag picker for card-specific triggers.
- Stop loading the ambiguous `Card activity` event entity for new installations.
- Fix the startup banner to display the actual app version.
- Preserve the low-level add-on events for backward compatibility.

## 1.4.4

- Explicitly disconnect the temporary card connection immediately after reading the UID.
- Use `SCARD_LEAVE_CARD` so releasing the software handle does not reset or power down the NFC card.
- Start removal monitoring only after the UID-reading connection is released.
- Add millisecond timestamps to reader and Home Assistant event logs.
- Measure and log Home Assistant event-delivery latency.
- Include the monotonic removal-detection timestamp in removal event data for diagnostics.

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
