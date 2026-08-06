# ACR122U NFC Reader

This app reads card UIDs from an ACS ACR122U connected directly to the Home Assistant host.

## Setup

1. Connect the ACR122U before starting the app.
2. Install the app.
3. Disable Protection mode.
4. Enable Start on boot and Watchdog.
5. Start the app.

## Test events

Open **Developer Tools → Events** and listen for:

- `acr122u_card_present`
- `acr122u_card_removed`

## Example automation

```yaml
alias: NFC demo
triggers:
  - trigger: event
    event_type: acr122u_card_present
    event_data:
      uid: C8149FEF
    id: placed

  - trigger: event
    event_type: acr122u_card_removed
    event_data:
      uid: C8149FEF
    id: removed

actions:
  - choose:
      - conditions:
          - condition: trigger
            id: placed
        sequence:
          - action: media_player.play_media
            target:
              entity_id: media_player.vlc_telnet
            data:
              media_content_id: media-source://media_source/local/demo/welcome.mp3
              media_content_type: music

      - conditions:
          - condition: trigger
            id: removed
        sequence:
          - action: media_player.media_stop
            target:
              entity_id: media_player.vlc_telnet

mode: restart
```

## Troubleshooting

`LIBUSB_ERROR_IO` usually means Protection mode is still enabled or another process already has the reader open.
