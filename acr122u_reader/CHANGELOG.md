# Changelog

## 1.1.0

- Emit `acr122u_card_present` when a card is placed.
- Emit `acr122u_card_removed` when a card is removed.
- Include the UID and reader name in both events.
- Add duplicate-scan cooldown configuration.

## 1.0.1

- Use an explicit Home Assistant base image.
- Restrict architecture to `aarch64`.

## 1.0.0

- Initial ACR122U reader implementation.
