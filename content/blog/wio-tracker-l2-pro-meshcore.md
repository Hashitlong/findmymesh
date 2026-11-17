---
title: "Seeed Wio Tracker L2 Pro and MeshCore: wait before you buy"
date: 2026-11-17
summary: Seeed's new touchscreen handheld is $69.90 and looks like a T-Deck Plus rival. It ships for Meshtastic, and MeshCore support is not in an official release yet. Here is what is confirmed and what is not.
category: News
products:
  - name: Seeed Wio Tracker L1 Pro
    amazon: https://www.amazon.com/dp/B0H2GRDBFL?tag=findmymesh-20
    verdict: Still the Seeed radio to buy for MeshCore today. Supported in the official flasher, runs for days.
  - name: LILYGO T-Deck Plus (915 MHz)
    amazon: https://www.amazon.com/dp/B0DSFR1XW5?tag=findmymesh-20
    verdict: The standalone MeshCore handheld you can flash right now. Has a keyboard, which the L2 Pro does not.
---

Seeed has a new handheld out, the [Wio Tracker L2 Pro](https://www.seeedstudio.com/Wio-Tracker-L2-Pro-for-Meshtastic-p-0000.html). It has a 3.2-inch touchscreen, GPS, a 3000 mAh battery and offline maps, and Seeed lists it at $69.90. People in MeshCore groups are already asking whether to buy one.

I do not have one yet, so this is not a review. Everything below comes from Seeed's product page and wiki, and from the [first look at NodakMesh](https://nodakmesh.org/blog/seeed-wio-tracker-l2-first-look), whose author had a pre-release unit and wrote the MeshCore port for it. I will update this post when I have used one.

## The short answer for MeshCore

**Do not buy it for MeshCore yet unless you are happy to wait or to flash test builds.**

As of November 16, 2026:

- Seeed sells it as a Meshtastic device. The product page does not mention MeshCore.
- No official MeshCore release supports it. A pull request adding companion, repeater and room server builds (number 3381 in the MeshCore repository) is waiting for review. It could be changed or turned down.
- According to NodakMesh, the MeshCore web flasher lists the L2 Pro only for Ripple GUI, a separate on-device firmware with paid unlocks. That is not the same thing as the open-source companion firmware most of us run.
- Even on Meshtastic, support is new. NodakMesh reports it arrived in the 2.8 series, which is still an alpha, and that the stable release has no L2 build.

So the hardware is on sale ahead of the firmware. That usually sorts itself out in a few weeks or months, but nobody can promise a date.

## What the hardware is

From Seeed's spec sheet:

- **Processor:** ESP32-S3, with 16 MB flash and 8 MB PSRAM
- **Radio:** SX1262, 863 to 928 MHz, 20 dBm maximum transmit power
- **Screen:** 3.2-inch IPS touchscreen. There is no keyboard.
- **GPS:** L76K, the same receiver as the L1 Pro
- **Battery:** 3000 mAh built in, USB-C charging, plus a solar input
- **Extras:** microSD slot for offline map tiles, speaker and microphone, Wi-Fi, a Grove port and a tripod thread
- **Antenna:** a folding external LoRa antenna. An RP-SMA to SMA adapter comes in the box.
- **Size and weight:** 87.5 x 69 x 26.6 mm with the antenna folded, 171.5 g

There is also a plain "L2" on Seeed's wiki with no case and no built-in battery. It is marked coming soon. The L2 Pro is the one you can order.

## How it compares to the L1 Pro

The names make it sound like an upgrade. It is really a different kind of radio.

The [L1 Pro](/blog-t-deck-plus-vs-wio-tracker-l1-pro) is an nRF52840 board with a small screen. You pair it to your phone and it runs for days. The L2 Pro is an ESP32-S3 board with a big backlit touchscreen, built to be used on its own without a phone.

That difference shows up in battery life. Seeed has not published a runtime figure for the L2 Pro, and NodakMesh did not measure one on the pre-release unit. ESP32-S3 radios with lit screens draw far more than nRF52 radios, so I would expect to charge it daily, the way I do a T-Deck Plus. That is my expectation, not a measurement.

The L2 Pro also transmits at 20 dBm against the L1 Pro's 22 dBm. In practice the antenna matters more than those 2 dB.

## How it compares to the T-Deck Plus

This is the real comparison. Both are ESP32-S3 standalone handhelds with GPS.

- **The L2 Pro has the bigger battery:** 3000 mAh against 2000 mAh.
- **The L2 Pro has an external antenna as standard.** The standard T-Deck Plus has an internal one.
- **The L2 Pro has the bigger screen:** 3.2 inches against 2.8.
- **The T-Deck Plus has a keyboard.** The L2 Pro is touch only.
- **The T-Deck Plus runs MeshCore today,** straight from the official flasher.

On paper the L2 Pro fixes two of my complaints about the T-Deck Plus, the antenna and the battery. Whether it is the better MeshCore handheld depends on firmware that has not shipped.

## What I would do

- **You want a MeshCore radio this week:** buy the L1 Pro to pair with your phone, or the T-Deck Plus to use on its own. Both are supported now.
- **You like new hardware and do not mind waiting:** the L2 Pro is a reasonable gamble at $69.90, and it works on Meshtastic alpha builds in the meantime.
- **You are buying for someone who is not a radio person:** not this one, not yet.

Prices and firmware support change. Check Seeed's page and the MeshCore flasher before you order.
