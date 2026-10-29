---
title: T-Deck Plus vs Wio Tracker L1 Pro: the two companions people actually argue about
date: 2026-11-22
summary: One has a keyboard and runs without a phone. The other runs for days and takes a real antenna. I carry both, and the right one depends on a single question.
category: Comparisons
products:
  - name: LILYGO T-Deck Plus (915 MHz)
    amazon: https://www.amazon.com/dp/B0DSFR1XW5?tag=findmymesh-20
    verdict: Buy it to chat on the device itself. Charge it every day.
  - name: Seeed Wio Tracker L1 Pro
    amazon: https://www.amazon.com/dp/B0H2GRDBFL?tag=findmymesh-20
    verdict: Buy it to pair with your phone and forget about charging for days.
  - name: Meshtastic T-Deck case with GPS space and SMA
    amazon: https://www.amazon.com/dp/B0DH88WY3C?tag=findmymesh-20
    verdict: The T-Deck needs a case; this one leaves room for the antenna connector.
  - name: muzi works 17 cm 915 MHz whip (SMA)
    amazon: https://www.amazon.com/dp/B0D7D6866W?tag=findmymesh-20
    verdict: Put one on whichever radio you buy.
---

These two come up in every "what should I buy" thread in every MeshCore group. They cost about the same, they are both handhelds with a screen and GPS, and they are built for completely different habits.

The question that decides it: **when you want to send a message, is your phone already in your hand?**

If yes, the L1 Pro. If you want to leave the phone in your pocket, or you want a radio that works when the phone is dead, the T-Deck Plus.

## What they share

Both are 915 MHz SX1262 radios that pair to the MeshCore app over Bluetooth. Both have GPS. Both have a screen. Both are in the official flasher. Both ship with an antenna that you should replace.

## Where the T-Deck Plus wins

**It is a standalone messenger.** The T-Deck Plus is the one mainstream MeshCore radio with a keyboard, and it can run a standalone interface on its own 2.8-inch display. You can read channels, send direct messages, and see who is around without touching a phone. For a lot of people that is the entire appeal of mesh radio: a device that is not a phone.

**The screen is readable.** 2.8 inches of color LCD versus a 0.96-inch OLED. You can actually read a conversation on it.

## Where the Wio Tracker L1 Pro wins

**Battery.** The L1 Pro is an nRF52840 board; the T-Deck Plus is an ESP32-S3 driving a backlit LCD. The L1 Pro's 2000 mAh class battery runs for days as a companion. The T-Deck's 2000 mAh battery runs for a day of real use. Same capacity, very different chip.

**Antenna.** The L1 Pro has an SMA connector on the outside of the case. The standard T-Deck Plus has an internal antenna; LILYGO sells an external-antenna variant, and it is the one to look for, but it is often out of stock. With a tuned whip on the L1 Pro, it hears repeaters the T-Deck can't.

**Ruggedness.** The L1 Pro comes in a finished case with a lanyard point. The T-Deck Plus is a bare board in a thin shell and wants a case from day one.

**Repeat mode.** MeshCore's optional Companion Repeat Mode, which lets a companion relay under special off-grid settings, was written up on the MeshCore blog specifically for the L1 Pro. If you are building a small private mesh for a hike or an event, that matters.

## Where they tie

GPS: both have it. Price: close enough that it should not decide. Firmware support: both are first-class in the flasher.

## My setup

The L1 Pro is the radio clipped to my bag. The T-Deck Plus lives in the truck's center console on a USB cable, where its battery life does not matter and its screen does. If I could only keep one, it would be the L1 Pro, because a companion that is dead is not a companion.

If you buy the T-Deck Plus, buy the case with the SMA cutout and plan to charge it nightly. If you buy the L1 Pro, install the OTAFIX bootloader the day it arrives so you can update it over Bluetooth later; the flasher warns you about this and it is easier to do before you depend on the radio.

## Further reading

For the T-Deck family itself (T-Deck vs Plus vs Pro, internal vs external antenna), our sister site Prepped Gear has a [full T-Deck Plus review](https://preppedgear.com/lilygo-t-deck-plus-review/).
