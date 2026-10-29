---
title: What to buy first for MeshCore: two starter kits, one cheap and one you'll keep
date: 2026-10-29
summary: You need a 915 MHz radio, the free app, a better antenna, and a repeater you can hear. Here is the exact shopping list for a first week, at two budgets.
category: How-to
products:
  - name: Heltec WiFi LoRa 32 V3
    amazon: https://www.amazon.com/dp/B0D1H1FN9Y?tag=findmymesh-20
    verdict: The cheap kit's radio. Works, teaches you the basics, moves to a shelf later.
  - name: Meshnology case for Heltec V3
    amazon: https://www.amazon.com/dp/B0F7R84CML?tag=findmymesh-20
    verdict: The cheap kit's case. Protects the screen and the antenna connector.
  - name: muzi works 17 cm 915 MHz whip (SMA)
    amazon: https://www.amazon.com/dp/B0D7D6866W?tag=findmymesh-20
    verdict: Both kits. The first upgrade, bought on day one.
  - name: Seeed Wio Tracker L1 Pro
    amazon: https://www.amazon.com/dp/B0H2GRDBFL?tag=findmymesh-20
    verdict: The keeper kit's radio. Finished, rugged, long battery, ships with MeshCore.
---

People overthink the first purchase. You do not need a repeater, a solar panel, or a keyboard radio to start. You need one companion radio that can hear a repeater somebody else already put up, and most of the U.S. groups on this site have those. Check your state page first; if there is a group near you, join their chat and ask what channel and settings they use before you buy anything.

Then buy one of these two kits.

## Kit 1: the cheap one

**Heltec WiFi LoRa 32 V3, a case, a tuned whip, and a USB-C cable you already own.**

The V3 is an ESP32-S3 board with an SX1262 radio and a little OLED. It is the board most of the people in your local group started on. Flash it as a Bluetooth companion at flasher.meshcore.io (Chrome or Edge on a desktop), install the MeshCore app on your phone, pair, set the U.S. preset, done.

Why the case: the OLED is glued to the top of the bare board and the SMA connector is the first thing that snaps off in a bag. Why the whip: the stubby antenna in the box is tuned somewhere near 915 MHz and not well. The 17 cm whip is the single biggest range gain you can buy.

What this kit does not do: run on a battery for long. The V3 has a battery connector but the ESP32 is thirsty. Power it from a USB battery bank in your bag, or plug it in at a window. When you buy a real companion later, the V3 becomes a room server or a bench repeater, so nothing is wasted.

## Kit 2: the one you'll keep

**Seeed Wio Tracker L1 Pro and a tuned whip.**

The L1 Pro is an nRF52840 radio with GPS, an OLED, a battery and a case, already assembled, and the listing above ships it flashed with MeshCore. Pair it with the app and it works. The nRF52 chip means it runs for days instead of hours. It has an SMA port, so the whip goes straight on.

It costs more than the whole cheap kit. It is also the radio you will still be carrying a year from now, which the V3 is not.

## What both kits need that isn't on Amazon

- **The MeshCore app**, free, from the App Store, Google Play, or meshcore.io for desktop.
- **A desktop browser** for the one-time flash (the L1 Pro on that listing arrives flashed; the V3 needs it).
- **The U.S. radio preset.** In the app's settings, choose the preset for your region. Your local group may use different settings; if so, use theirs.
- **Someone to talk to.** A companion does not relay, so on its own it only reaches other radios in direct range. Find the repeaters near you on your state page or the live map before you decide the radio "doesn't work."

## What to buy second

Not a second companion. A repeater, if your area needs one, or a better antenna for the one you have. The repeater board comparison and the solar parts list on this site cover that. Until then, one good companion and a group that already has repeaters is the whole hobby.
