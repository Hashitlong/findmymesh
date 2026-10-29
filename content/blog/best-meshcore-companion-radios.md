---
title: The best MeshCore companion radios, from what I actually carry
date: 2026-11-01
summary: Six companions I've run on the Lake Norman mesh, ranked by what they're good at. There is no single best one; there is a best one for how you use it.
category: Comparisons
products:
  - name: LILYGO T-Deck Plus (915 MHz)
    amazon: https://www.amazon.com/dp/B0DSFR1XW5?tag=findmymesh-20
    verdict: Best standalone. Keyboard, screen, GPS, no phone needed.
  - name: Seeed SenseCAP T1000-E
    amazon: https://www.amazon.com/dp/B0DJ6KGXKB?tag=findmymesh-20
    verdict: Best pocket companion. Card-sized, waterproof, forgettable in a good way.
  - name: Seeed Wio Tracker L1 Pro
    amazon: https://www.amazon.com/dp/B0H2GRDBFL?tag=findmymesh-20
    verdict: Best all-rounder. Rugged, low power, external antenna.
  - name: LILYGO T-Echo
    amazon: https://www.amazon.com/dp/B0B659536P?tag=findmymesh-20
    verdict: Best battery life per dollar. E-paper and nRF52.
  - name: Elecrow ThinkNode M1
    amazon: https://www.amazon.com/dp/B0FPLWYB8R?tag=findmymesh-20
    verdict: Good finished e-paper companion if the T-Echo is sold out.
  - name: Heltec WiFi LoRa 32 V3
    amazon: https://www.amazon.com/dp/B0D1H1FN9Y?tag=findmymesh-20
    verdict: Cheapest way in. Fine plugged in, poor on battery.
---

A companion is the radio you carry. It talks to the MeshCore app on your phone over Bluetooth (or, on a couple of these, shows chats on its own screen) and it does not relay anyone else's traffic. That matters for how you shop: a companion does not need to be high up or high power. It needs to be with you, charged, and comfortable to use.

I've carried every one of these. Here is where each one lands.

## Quick answer

- **Want to chat without pulling out your phone?** T-Deck Plus.
- **Want something you forget is in your pocket?** T1000-E.
- **Want one radio that does everything reasonably?** Wio Tracker L1 Pro.
- **Want the longest battery life?** T-Echo.
- **Want to spend as little as possible?** Heltec V3, plugged into a USB battery.

## LILYGO T-Deck Plus

The T-Deck Plus is an ESP32-S3 handheld with a 2.8-inch screen, a thumb keyboard, GPS and a built-in 2000 mAh battery. It is the only radio on this list that can run a standalone MeshCore interface on its own display, so you can read and send messages without a phone. That is the whole reason to buy it.

The trade-offs are real. It is the biggest and heaviest thing here. The ESP32 draws more than the nRF52 radios, so a day of use is realistic and a week is not. The stock antenna is mediocre; the version with an external antenna connector is the one to get if you can find it, and a tuned 915 MHz whip helps either version.

Buy it if you want a self-contained messenger. Skip it if your phone is always in your hand anyway.

## Seeed SenseCAP T1000-E

Credit-card sized, IP65, GPS, 700 mAh battery, no screen, no external antenna. It pairs to the phone and otherwise gets out of the way. It is the radio I hand to people who are new, because there is nothing to break and nothing to configure on the device itself.

The lack of an antenna port is the limit. Range is noticeably shorter than a radio with a proper whip, especially indoors. It is a town radio, not a hilltop radio. It also ships Meshtastic-branded; the MeshCore flasher supports it, and you flash it over USB like anything else.

## Seeed Wio Tracker L1 Pro

nRF52840, SX1262, GPS, OLED, 2000 mAh class battery, SMA antenna port, and it comes in a finished case. The listing above ships it flashed with MeshCore. It is the radio that does the fewest things wrong: the nRF52 keeps battery life long, the SMA port means you can put a real antenna on it, and the screen shows enough to know what is going on.

Text entry is through buttons, so this is a phone-paired companion, not a keyboard device. One note from the repeater guide: on this board the factory bootloader can't do Bluetooth firmware updates, and the official flasher tells you to install the OTAFIX bootloader first. Do that on day one.

## LILYGO T-Echo

nRF52840, SX1262, 1.54-inch e-paper, GPS, 850 mAh built in. The e-paper screen costs almost nothing to keep on, and the nRF52 sleeps well, so this is the companion that still has charge when you forgot about it for a week.

The screen is small and the three buttons take some learning. It is also a device that goes in and out of stock in waves. If you can't find it, the ThinkNode M1 below is the same idea.

## Elecrow ThinkNode M1

Same recipe as the T-Echo: nRF52840, 1.54-inch e-paper, GPS, 1200 mAh battery, finished case. Elecrow sells it with MeshCore support, and the flasher lists it by name. I keep one as a spare and it has done nothing to complain about. If both are in stock, I'd take the T-Echo for the LILYGO track record and the M1 for the bigger battery; it is close.

## Heltec WiFi LoRa 32 V3

Not a handheld. A bare ESP32-S3 board with an OLED and an SMA connector. You add a battery or a USB power bank and ideally a case. It is on this list because it is the cheapest working MeshCore radio you can buy, and because almost everyone's first node is one.

As a companion it works. The ESP32 drinks battery, the board is fragile without a case, and the screen is tiny. Use it to learn, then move it to a mains-powered room server or a bench repeater when you buy a real companion.

## How I'd spend the money

If you are buying one radio: Wio Tracker L1 Pro. If you are buying two: add a T1000-E for the car or for a family member. If you find yourself wanting to type without a phone, that is when the T-Deck Plus earns its place.

Whatever you buy, swap the stubby antenna for a tuned 915 MHz whip. It is the cheapest range upgrade there is.
