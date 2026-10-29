---
title: Best boards for a MeshCore repeater: why nRF52 wins on a roof
date: 2026-11-10
summary: A repeater runs 24 hours a day on whatever power you can get to it. That one fact decides the board. Here is what I put up and why.
category: Comparisons
products:
  - name: RAK WisBlock Mini Meshtastic Starter Kit (RAK4631, US915)
    amazon: https://www.amazon.com/dp/B0DFMMTQZM?tag=findmymesh-20
    verdict: My default rooftop board. nRF52840, lowest draw, battery and solar on the base board.
  - name: Heltec Mesh Node T114 (kit with case and battery)
    amazon: https://www.amazon.com/dp/B0F3X3WNJP?tag=findmymesh-20
    verdict: Easiest nRF52 repeater for a first build. Screen, battery and solar connectors included.
  - name: Seeed XIAO nRF52840 & Wio-SX1262 Kit
    amazon: https://www.amazon.com/dp/B0FJWRHG8K?tag=findmymesh-20
    verdict: Smallest and cheapest. You supply everything else.
  - name: Seeed SenseCAP Solar Node P1-Pro (MeshCore)
    amazon: https://www.amazon.com/dp/B0H2GSYN3B?tag=findmymesh-20
    verdict: The no-build option. Panel, cells, box and radio in one piece.
  - name: Heltec WiFi LoRa 32 V4
    amazon: https://www.amazon.com/dp/B0FS1R4HXH?tag=findmymesh-20
    verdict: Only for repeaters with wall power. Strong transmitter, hungry chip.
---

In MeshCore, only repeaters relay traffic. Your companion radios do not forward anything. So the repeaters are the network, and a repeater that browns out at 3 a.m. in January takes a chunk of the map with it. Everything below follows from that.

## The one rule: nRF52 for anything on a battery

MeshCore boards come in two families. ESP32 boards (Heltec V3 and V4, T-Deck, T-Beam, Station G3) have Wi-Fi and a lot of horsepower, and they burn power at idle. nRF52840 boards (RAK4631, Heltec T114, Seeed XIAO nRF52840, T-Echo, Wio Tracker) have no Wi-Fi, less horsepower, and sip. A repeater does not need Wi-Fi or horsepower. It needs to sit there listening for months.

This is why nearly every solar repeater you see on the community map is an nRF52 board, and why the ESP32 boards on this list have "wall power" next to them.

## RAK WisBlock RAK4631

The RAK4631 is an nRF52840 plus SX1262 on a small core module that plugs into a WisBlock base board. The base board brings the battery connector, solar input and USB-C. The Mini starter kit (RAK19003 base) in the link above is the small one; the Basic kit with the RAK19007 base is bigger and easier to work on. Both are in the MeshCore flasher under RAK WisBlock / WisMesh.

Why it is my default: it has the lowest idle current of anything I have put on a roof, the modular connectors make a clean build, and RAK publishes real documentation. Two cautions. It ships flashed with Meshtastic, so you will reflash it before it does anything useful for MeshCore. And the Mini base's connectors are small; if you have big hands, buy the Basic kit.

## Heltec Mesh Node T114

nRF52840 plus SX1262, with a 1.14-inch TFT screen and both a battery connector and a solar panel connector on the board. The kit linked above includes a case and a battery, which is most of a first repeater in one box. Heltec's own page names MeshCore, and the flasher lists it.

It draws a little more than the RAK because of the screen, and the screen is pointless on a roof; turn it off in config. For a first repeater, or one in an attic or a window where you want to glance at it, this is the easiest path.

Flashing note: the official flasher recommends the OTAFIX bootloader on the T114 before you rely on over-the-air updates. Do it before the board goes up.

## Seeed XIAO nRF52840 and Wio-SX1262

A thumb-sized nRF52840 board and a matching SX1262 radio board. No screen, no case, no battery, no GPS unless you add the L76K module. Cheapest nRF52 repeater you can build and the smallest. It is also the same radio core that Seeed uses inside the finished P1-Pro solar node below, which tells you it holds up outdoors.

Buy this if you enjoy the build. You will be adding a battery, a charge controller, a case and an antenna adapter, and that adds up to more than the kit.

## Seeed SenseCAP Solar Node P1-Pro

The finished product: XIAO nRF52840 core, SX1262, L76K GPS, a 5 W panel on the lid, and four 18650 cells, all in an IPX6 enclosure with an N-type antenna port. The listing above is the MeshCore-flashed version. Mount it, point the panel south, done.

It costs about what the RAK build costs by the time you have bought the panel, cells, box and controller separately, and it saves you the weekend. The panel is the limit: 5 W is enough in Carolina sun, and marginal in a northern winter under trees. You cannot easily swap in a bigger panel without opening it up.

## Heltec WiFi LoRa 32 V4

Here for one case: a repeater that has wall power, like a second-floor window or a shed with an outlet. The V4's amplified radio (27 to 28 dBm versus 22 dBm on an nRF52 board's SX1262) makes it a loud repeater, and on mains power its appetite doesn't matter. Put it on a battery and you will be climbing a ladder to swap it.

## What I'd actually buy

- First repeater, learning as you go: **T114 kit**.
- Rooftop solar build: **RAK4631** with a 10 W panel and a Waveshare controller (parts list in the solar repeater article).
- No desire to build anything: **P1-Pro**.
- Indoor with an outlet: **Heltec V4**.

Then put the money you saved into the antenna, which matters more than any of this.
