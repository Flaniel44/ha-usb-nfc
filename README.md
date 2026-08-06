# ACR122U NFC Reader for Home Assistant

A Home Assistant add-on that turns an **ACS ACR122U USB NFC reader** into a native Home Assistant device.

Unlike existing solutions, this project is designed to work **entirely offline** with Home Assistant OS and supports:

- 📇 Native Home Assistant Tags
- 📡 Card placed / card removed events
- 🎛 Native device triggers in the Automation UI
- 🔖 Automatic tag registration
- 🔌 USB ACR122U support
- 🌐 No cloud required
- 📶 No MQTT required
- 🏠 Fully local

---

# Features

- Detect NFC cards using an ACS ACR122U
- Fire events when a card is placed on or removed from the reader
- Automatically register scanned cards as Home Assistant Tags
- Expose:
  - Binary sensor: Card Present
  - Sensor: Current Tag
  - Sensor: Last Tag
- Native Automation UI support
- Runs entirely on Home Assistant OS

---

# Requirements

- Home Assistant OS
- ACS ACR122U USB NFC Reader
- USB NFC tags/cards

---

# Installation

## 1. Add this repository

Open:

**Settings → Add-ons → Add-on Store**

Click the **⋮** menu → **Repositories**

Add:

```
https://github.com/Flaniel44/home-assistant-acr122u
```

---

## 2. Install

Install **ACR122U NFC Reader**.

---

## 3. Disable Protection Mode

Open the add-on configuration and disable:

- Protection mode

This is required so the add-on can access the USB smart card reader.

---

## 4. Enable automatic startup

Enable:

- Start on boot
- Watchdog

Start the add-on.

---

## 5. Restart Home Assistant

The add-on installs the bundled custom integration automatically.

Restart Home Assistant once.

---

## 6. Add the integration

Go to

**Settings → Devices & Services**

Click

**Add Integration**

Search for

```
ACR122U NFC Reader
```

Complete the setup.

---

# Usage

After installation you'll see a new device:

```
ACR122U NFC Reader
```

with the following entities:

- Card Present
- Current Tag
- Last Tag

Unknown NFC cards will automatically appear under:

```
Settings → Tags
```

where they can be renamed and used throughout Home Assistant.

---

# Automation Examples

## Trigger when a card is placed

Choose

```
Device
    ACR122U NFC Reader
        Card placed
```

## Trigger when a card is removed

Choose

```
Device
    ACR122U NFC Reader
        Card removed
```

---

# Events

The add-on also fires these events for advanced automations:

```
acr122u_card_present
acr122u_card_removed
```

---

# Roadmap

- Multiple reader support
- Per-tag actions
- LED control
- Buzzer control
- Write NFC tags
- Home Assistant Assist integration
- Blueprint library

---

# License

MIT
