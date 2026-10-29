---
title: A MeshCore node for the truck: mag-mount antenna, always-on power, and which radio
date: 2026-11-25
summary: A vehicle node reaches repeaters your pocket radio can't, because the antenna is on the roof. Here's the simple version that doesn't involve drilling.
category: Builds
products:
  - name: LILYGO T-Beam Supreme (915 MHz, L76K GPS)
    amazon: https://www.amazon.com/dp/B0CXJ71NB6?tag=findmymesh-20
    verdict: The classic vehicle board. GPS, 18650 holder, SMA, runs happily on USB.
  - name: Seeed Wio Tracker L1 Pro
    amazon: https://www.amazon.com/dp/B0H2GRDBFL?tag=findmymesh-20
    verdict: If you'd rather use the companion you already own, on a longer cable.
  - name: 5.8 dBi magnet-base 915 MHz antenna
    amazon: https://www.amazon.com/dp/B09MRGDTPZ?tag=findmymesh-20
    verdict: The part that makes a vehicle node worth doing. Roof, not dash.
  - name: SMA to N adapter kit (4 pack)
    amazon: https://www.amazon.com/dp/B06XPDWBPR?tag=findmymesh-20
    verdict: Check the mag mount's connector; you may need one.
---

A companion in your pocket inside a vehicle is in a metal box with the antenna at knee height. A companion with its antenna on the roof is a different radio. Everything else about this build is just keeping that antenna fed.

## The antenna is the build

A magnet-base 915 MHz antenna on the roof (or the trunk lid, or the hood) gets the antenna outside the metal and above the glass. The one in the list is a 5.8 dBi whip on a magnetic base with a cable that routes through a door seal. Put it in the middle of the roof if you can; the roof acts as a ground plane and the middle is where it works best.

Check the connector on the cable end. These often come as SMA-male, which goes straight onto a board, but some are N or RP-SMA. Have the adapter kit on hand, and make sure nothing in the chain is reverse-polarity.

## The radio

**T-Beam Supreme.** ESP32-S3, SX1262, L76K GPS, an 18650 battery holder and an SMA connector. It is the board people have been putting in vehicles since before MeshCore existed, and the flasher lists it. Power it from a USB port that is live when the truck is on; the 18650 keeps it up through engine starts and short stops. The ESP32 draw does not matter when the alternator is paying for it.

**Wio Tracker L1 Pro.** If you already carry one, it works just as well. Put it on a USB cable, connect the mag-mount cable to its SMA port, and it becomes the vehicle node while you drive and your pocket node when you get out. The only cost is unscrewing the antenna each time.

Either way, pair the vehicle node to your phone over Bluetooth like any companion. If you want to see messages on a screen in the cab, the T-Deck Plus on a USB cable is the option with a real display, as covered in the companion comparison.

## Power

Use a USB port that switches off with the ignition, or you will come back to a dead battery in a week. Boards with a battery (the Supreme's 18650, the L1 Pro's internal pack) ride through the gaps. Boards without one, like a bare Heltec V3, will reboot every time the truck does and lose their place in the mesh for a minute.

## Mounting

The board goes in the console or a cubby, not on the dash in the sun. ESP32 boards get warm on their own and a July dashboard in Carolina will cook a lithium cell. Zip-tie the antenna cable so it is not the thing that gets yanked when the door closes.

## What you'll notice

The first drive with a roof antenna is when you find out how many repeaters are actually around you. Paths that showed two or three hops from a pocket radio drop to one. Repeaters you never heard from show up in adverts. That is the whole reason for the build, and it costs an antenna and a USB cable.
