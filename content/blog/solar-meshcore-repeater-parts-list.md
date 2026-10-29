---
title: Solar MeshCore repeater: the parts list I use
date: 2026-11-13
summary: Every part in the box, with the reason it's there. Buy this list once and you have a repeater that runs through the winter.
category: Builds
products:
  - name: RAK WisBlock Mini Meshtastic Starter Kit (RAK4631, US915)
    amazon: https://www.amazon.com/dp/B0DFMMTQZM?tag=findmymesh-20
    verdict: The radio. nRF52840, low draw, battery and solar inputs on the base.
  - name: Voltaic Systems 10 W 6 V ETFE solar panel
    amazon: https://www.amazon.com/dp/B085W9KCZ8?tag=findmymesh-20
    verdict: The panel. 10 W is twice what a bare repeater needs, which is the margin for December.
  - name: Waveshare Solar Power Manager (D)
    amazon: https://www.amazon.com/dp/B0CT2ZBML9?tag=findmymesh-20
    verdict: The charge controller. Panel in, lithium pack charged, regulated 5 V out.
  - name: TICONN IP67 ABS enclosure (8.7 x 6.7 x 4.3 in)
    amazon: https://www.amazon.com/dp/B0B87V7QTH?tag=findmymesh-20
    verdict: The box. Big enough to work in, with room for a bulkhead connector.
  - name: Waterproof 5.8 dBi 915 MHz fiberglass antenna (N-type)
    amazon: https://www.amazon.com/dp/B0GBSTPHKG?tag=findmymesh-20
    verdict: The antenna. Outdoor, omnidirectional, N connector.
  - name: N-type lightning arrestor (N-male / N-female)
    amazon: https://www.amazon.com/dp/B07JY6TD2T?tag=findmymesh-20
    verdict: Between the antenna and the box, grounded.
  - name: Times Microwave LMR-400 N-male to N-male, 25 ft
    amazon: https://www.amazon.com/dp/B07Q86WGV3?tag=findmymesh-20
    verdict: The feedline, if the antenna has to be away from the box.
  - name: SMA to N adapter kit (4 pack)
    amazon: https://www.amazon.com/dp/B06XPDWBPR?tag=findmymesh-20
    verdict: Board is SMA, world is N. You need these.
  - name: Reversible J-pole antenna mount (2 pack)
    amazon: https://www.amazon.com/dp/B09XPHRNWK?tag=findmymesh-20
    verdict: Holds the antenna and the panel off an eave or wall.
---

This is the build I put on roofs around Lake Norman. It is not the cheapest possible solar repeater and it is not the fanciest. It is the one that does not need me to climb back up.

If you'd rather not build, the Seeed P1-Pro is the same idea in one sealed box and is on the repeater board comparison. This article is for the people who want to pick each part.

## The radio: RAK4631 on a WisBlock base

See the repeater board article for why an nRF52840 board and not an ESP32. Short version: the ESP32 boards draw several times more at idle, and idle is what a repeater does all night. The RAK4631 core on the WisBlock base gives you a battery connector and a solar input on the board, so the controller below could even be skipped on a small build. I keep the controller because it lets me use a bigger panel and a bigger pack than the base board is designed for.

Flash it as a Repeater at flasher.meshcore.io, set the U.S. radio preset over USB (the repeater guide on this site has the exact command), set an admin password, and test it on the bench for a few days before it goes outside.

## Power: 10 W panel, Waveshare controller, lithium pack

A MeshCore repeater on an nRF52 board averages a small fraction of a watt. A 10 W panel is overkill in June and about right in December, when the sun is low, the days are short, and a week of clouds happens. Buy the panel for the worst month, not the best.

The Voltaic panel costs more than the no-name 10 W panels. The reason to pay it is the ETFE face: cheap panels cloud and delaminate after a year outside, and then you are back on the ladder. Voltaic's have held up.

The Waveshare Solar Power Manager (D) takes 6 to 24 V from the panel, charges a lithium pack, and puts out regulated 5 V over USB and a header. Pair it with a 3.7 V lithium pack sized for your winter: I use at least 10,000 mAh for a rooftop unit, which is several days of cloud with no sun at all. Use a pack with a protection board. Do not use loose 18650 cells in a holder outdoors unless you like troubleshooting intermittent contacts in the cold.

## The box

The TICONN IP67 box in the list is bigger than it needs to be, on purpose. You want to be able to get your hands in it on a ladder. Drill one hole for an N-type bulkhead connector (or an SMA bulkhead if you are keeping the antenna run short) and one for a cable gland for the panel lead. Mount the box in the shade of the panel if you can; heat is harder on lithium than cold.

Put a desiccant pack inside and replace it when you do your annual check.

## Antenna, feedline, arrestor

The 5.8 dBi fiberglass antenna is the common baseline for a fixed 915 MHz node. It is omnidirectional, it is weatherproof, and it has an N connector. Mount it vertical, as high as you can, with as little around it as possible. Height and a clear view beat gain every time.

If the antenna can sit right on the box, use a short jumper and skip the long feedline. If it has to be up a mast while the box stays low, use real LMR-400 (the Times Microwave listing, not a "KMR" look-alike) and keep it as short as possible; at 915 MHz, 25 feet of LMR-400 loses roughly a decibel, and cheap RG58 loses several.

The lightning arrestor goes in line between antenna and box and must be bonded to a ground rod or the house's grounding electrode. An ungrounded arrestor is a connector that costs twenty dollars.

Adapters: the RAK board is SMA, the arrestor and antenna are N. Buy the adapter kit and use the SMA-male to N-female piece. Check that nothing in the chain is RP-SMA (reverse polarity, common on Wi-Fi gear); it will not mate.

## Mounting

The reversible J-pole mount holds the antenna off an eave, fascia or wall and gives you a stub to clamp the panel bracket to. Lag bolt it into framing, not siding. Point the panel south, tilt it steeper than you think for winter, and make sure nothing shades it after 2 p.m.

## Before it goes up

- Run it on the bench on the actual battery and panel for a week in a window. Watch the voltage.
- Confirm you can reach it over the mesh with the app's remote management and the admin password.
- Write the repeater's name, key prefix and the date on tape inside the lid.
- Install the OTAFIX bootloader if the flasher recommends it for your board, so you can update it later without taking it down.

Then put it up and leave it alone. The best repeater is the one you forget about.
