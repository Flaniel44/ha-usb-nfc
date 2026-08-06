# ha-usb-nfc

A plug-and-play USB NFC solution for Home Assistant.

**ha-usb-nfc** brings USB NFC readers to Home Assistant with native device support, Home Assistant Tags, Automation UI triggers, and fully offline operation.

Unlike existing approaches, this project is designed specifically for **Home Assistant OS** and requires **no MQTT, Node-RED, ESPHome, external computers, or cloud services**.

> ⚠️ **Project Status**
>
> This project is currently in active development. While it is already functional, the API and feature set may evolve as support for additional USB NFC readers is added.

---

# Why?

The **ACS ACR122U** is one of the most common USB NFC readers available, yet Home Assistant has never had a simple, offline-first integration for it.

Most existing solutions require one or more of:

- MQTT
- ESPHome
- Node-RED
- Raspberry Pi scripts
- External computers
- Cloud services

The goal of **ha-usb-nfc** is to provide a polished, native Home Assistant experience that works entirely on a single Home Assistant OS installation.

Long term, the project aims to become the standard USB NFC solution for Home Assistant.

---

# Features

- ✅ USB NFC reader support
- ✅ Fully offline
- ✅ Native Home Assistant integration
- ✅ Automatic Home Assistant Tag registration
- ✅ Native Automation UI triggers
- ✅ Card present detection
- ✅ Card removed detection
- ✅ Binary sensor
- ✅ Current tag sensor
- ✅ Last scanned tag sensor
- ✅ No MQTT
- ✅ No Node-RED
- ✅ No cloud

---

# Supported Hardware

Currently supported:

- **ACS ACR122U**

Planned support:

- ACS ACR1252U
- PN532 (USB mode)
- HID Omnikey readers
- Sony RC-S380
- Other PC/SC-compatible USB NFC readers

---

# Installation

## 1. Add this repository

Open:

**Settings → Add-ons → Add-on Store**

Click the **⋮** menu → **Repositories**

Add:

```
https://github.com/Flaniel44/ha-usb-nfc
```

---

## 2. Install the add-on

Install:

**ACR122U NFC Reader**

---

## 3. Disable Protection Mode

Open the add-on configuration.

Disable:

- Protection mode

This is required so the add-on can communicate directly with the USB smart card reader.

---

## 4. Enable automatic startup

Enable:

- Start on boot
- Watchdog

Start the add-on.

---

## 5. Restart Home Assistant

The add-on automatically installs the bundled custom integration.

Restart Home Assistant once.

---

## 6. Add the integration

Go to:

**Settings → Devices & Services**

Click:

**Add Integration**

Search for:

```
ACR122U NFC Reader
```

Complete the setup.

---

# Usage

After installation a new device appears:

```
ACR122U NFC Reader
```

It exposes:

- Binary Sensor
  - Card Present

- Sensor
  - Current Tag

- Sensor
  - Last Tag

Unknown NFC tags automatically appear under:

```
Settings → Tags
```

They can then be renamed and used throughout Home Assistant.

---

# Automations

The integration adds native device triggers.

## Card placed

```
Trigger
    Device
        ACR122U NFC Reader
            Card placed
```

## Card removed

```
Trigger
    Device
        ACR122U NFC Reader
            Card removed
```

No custom YAML is required.

---

# Advanced Events

For advanced automations, the add-on also emits:

```
acr122u_card_present
acr122u_card_removed
```

These remain available for users who prefer event-based automations.

---

# AI Disclosure

This project was developed collaboratively by a human developer and AI.

The architecture, implementation, debugging, testing, documentation, and feature design were created through an iterative engineering process between the project author and OpenAI's ChatGPT.

Every feature was tested on real Home Assistant OS hardware before being incorporated into the project.

AI accelerated development, but the project direction, engineering decisions, testing, and final implementation were guided by the project author.

---

# Roadmap

## Reader Support

- ACR122U
- ACR1252U
- PN532 (USB)
- HID Omnikey
- Additional PC/SC readers

## Features

- Reader LED control
- Reader buzzer control
- Write NFC tags
- Read NDEF records
- Home Assistant Assist integration
- Blueprint library
- Multiple reader support

---

# Contributing

Bug reports, feature requests, and pull requests are always welcome.

If you have a USB NFC reader that isn't currently supported, please open an issue and include the model number and USB identifiers.

---

# License

MIT License
