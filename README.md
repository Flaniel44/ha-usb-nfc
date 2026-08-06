# ha-usb-nfc

> A plug-and-play USB NFC solution for Home Assistant.

**ha-usb-nfc** brings USB NFC readers to Home Assistant with native Tags, native Automation triggers, automatic device discovery, and completely offline operation.

Unlike existing solutions, **ha-usb-nfc** is designed specifically for **Home Assistant OS**.

No MQTT.

No Node-RED.

No ESPHome.

No HACS.

No external computer.

Just install the add-on, plug in a USB NFC reader, and start automating.

---

## Demo

> *(Coming soon)*

A short demo showing:

- Tap NFC card
- Light changes colour
- Audio begins playing
- Remove NFC card
- Audio stops

---

# Features

## Native Home Assistant Integration

- ✅ Native Home Assistant device
- ✅ Native Home Assistant Tags
- ✅ Native Device Triggers
- ✅ Native Event Entity
- ✅ Native Binary Sensor
- ✅ Native Sensors

No YAML required.

---

## NFC Events

Supports:

- ✅ NFC card scanned
- ✅ NFC card removed

Each event includes:

- UID
- Reader name

---

## Automation UI

Create automations directly from the Home Assistant UI.

Examples:

```
Device
    USB NFC Reader
        NFC card scanned
```

```
Device
    USB NFC Reader
        NFC card removed
```

Optionally choose:

- Any card
- A specific Home Assistant Tag

No manual UID entry required.

---

## Automatic Tag Registration

Unknown NFC cards are automatically added to:

```
Settings
    → Tags
```

Rename them once:

```
Welcome Card

Movie Card

Blue Demo Card
```

Then use those names everywhere in Home Assistant.

---

## Reader Status

The integration exposes:

| Entity | Purpose |
|---------|----------|
| Card Present | Whether a card is currently on the reader |
| Current Tag | UID currently on the reader |
| Last Tag | Most recently scanned card |
| Card Activity | Event entity for scans/removals |

---

## Startup Diagnostics

Every startup performs a complete health check.

Example:

```text
────────────────────────────────────
ha-usb-nfc v1.3.1
────────────────────────────────────

Running startup diagnostics...

✓ Home Assistant API

✓ USB subsystem

✓ ACR122U detected

✓ USB permissions

✓ Integration installed

Waiting for NFC cards...
```

The goal is simple:

**Users should never need to read cryptic log messages.**

---

## Helpful Notifications

Instead of silently failing, ha-usb-nfc guides the user.

Examples:

- Protection Mode enabled
- USB reader not connected
- Home Assistant restart required
- Integration successfully installed

Everything appears as native Home Assistant notifications.

---

# Installation

## 1. Add this repository

Open:

```
Settings
    → Add-ons
    → Add-on Store
```

Click:

```
⋮
Repositories
```

Add:

```
https://github.com/Flaniel44/ha-usb-nfc
```

---

## 2. Install the add-on

Install:

```
USB NFC Reader
```

---

## 3. Disable Protection Mode

Open the add-on.

Disable:

- Protection Mode

This allows direct USB access to supported readers.

If you forget, the add-on will notify you automatically.

---

## 4. Start the add-on

Enable:

- Start on boot
- Watchdog

Start the add-on.

---

## 5. Restart Home Assistant

If the bundled integration was installed or updated, the add-on will automatically create a persistent notification requesting a Home Assistant restart.

Restart Home Assistant once.

---

## 6. Add the Integration

Go to:

```
Settings
    → Devices & Services
```

Click:

```
Add Integration
```

Search for:

```
USB NFC Reader
```

---

# Creating Automations

## Trigger on any card

```
Device

USB NFC Reader

NFC card scanned
```

---

## Trigger on a specific card

Choose:

```
Tag

Welcome Card
```

or any other Home Assistant Tag.

No UID lookup required.

---

## Trigger when a card is removed

```
Device

USB NFC Reader

NFC card removed
```

Optionally select a specific Tag.

---

# Supported Hardware

Currently supported:

- ACS ACR122U

Planned:

- ACS ACR1252U
- PN532 (USB)
- HID Omnikey
- Sony RC-S380
- Other PC/SC-compatible USB NFC readers

---

# Troubleshooting

| Code | Meaning | Resolution |
|------|---------|------------|
| HUN-001 | USB reader detected but inaccessible | Disable Protection Mode |
| HUN-002 | USB reader not detected | Connect a supported reader |
| HUN-004 | Home Assistant API unavailable | Wait for Home Assistant to finish starting |
| HUN-005 | Integration installation failed | Verify Home Assistant configuration directory permissions |

---

# Why?

The ACS ACR122U is one of the world's most common USB NFC readers, yet Home Assistant has never had a polished, offline-first solution.

ha-usb-nfc aims to become the standard USB NFC integration for Home Assistant by providing a clean installation experience, native Home Assistant features, and support for additional USB NFC readers over time.

---

# Roadmap

## Completed

- Native Home Assistant integration
- Native Tags
- Native Device Triggers
- Native Event Entity
- Card scanned events
- Card removed events
- Automatic Tag registration
- Startup diagnostics
- Persistent notifications
- Automatic integration installation
- Offline operation

## In Progress

- Multiple reader support
- Automatic reader reconnect
- Better diagnostics

## Planned

- Reader LED control
- Reader buzzer control
- Write NFC tags
- Read NDEF records
- Blueprint library
- Home Assistant Assist support
- Additional USB NFC readers

---

# Contributing

Bug reports, ideas, feature requests, and pull requests are always welcome.

If you own a USB NFC reader that isn't currently supported, please open an issue with the model number and USB identifiers.

---

# AI Disclosure

This project was developed collaboratively by a human developer and AI.

OpenAI's ChatGPT was used throughout the design, implementation, debugging, documentation, and refinement of the project. AI significantly accelerated development by helping generate ideas, review code, identify issues, and iterate on solutions.

All architectural decisions, hardware validation, feature selection, testing, and final acceptance were performed by the project author using real Home Assistant OS hardware.

The goal of this disclosure is transparency. This project reflects a collaborative software engineering workflow where AI served as a development partner, while responsibility for the final product remains with the project author.

---

# License

MIT
