---
title: 915 MHz antennas for MeshCore: what to buy for a pocket, a window and a roof
date: 2026-11-04
summary: The antenna is the biggest range upgrade you can make and the cheapest. Three picks, one for each place a radio lives, and the mistakes that waste the money.
category: How-to
products:
  - name: muzi works 17 cm 915 MHz whip (SMA)
    amazon: https://www.amazon.com/dp/B0D7D6866W?tag=findmymesh-20
    verdict: For handhelds and companions. Tuned for 915, flexible, survives a pocket.
  - name: ALFA AOA-915-5ACM 5 dBi outdoor antenna
    amazon: https://www.amazon.com/dp/B08H8J6ZV6?tag=findmymesh-20
    verdict: For windows, balconies and compact outdoor spots. Short, weatherproof, N-male.
  - name: Waterproof 5.8 dBi 915 MHz fiberglass antenna (N-type)
    amazon: https://www.amazon.com/dp/B0GBSTPHKG?tag=findmymesh-20
    verdict: For roofs and masts. The standard fixed-repeater antenna.
  - name: SMA to N adapter kit (4 pack)
    amazon: https://www.amazon.com/dp/B06XPDWBPR?tag=findmymesh-20
    verdict: You will need at least one of these for any outdoor antenna.
---

Most MeshCore boards ship with a short stubby antenna that is tuned somewhere in the general neighborhood of 915 MHz and is there so the radio has a load on it. Replacing it is the first thing to do, before a second radio, before a repeater, before anything.

Here is what I put on each kind of radio.

## In your pocket: a tuned 17 cm whip

A quarter-wave whip for 915 MHz is about 8 cm; a half-wave is about 16 cm. The 17 cm whip in the list is a flexible half-wave-ish antenna with an SMA male connector, tuned for the U.S. band. On a T-Deck, a Heltec board in a case, or a Wio Tracker, the difference from the stock stub is obvious the first time you check RSSI on a message from the same repeater.

Keep it vertical when you can. A radio lying flat on a car seat with the antenna horizontal is throwing half its signal into the floor mat.

## In a window or on a balcony: the ALFA 5 dBi

The ALFA AOA-915-5ACM is a short outdoor antenna with an N-male connector, sold for 802.11ah and LoRa, which is the same band. It is about the size of a highlighter, weatherproof, and it does not look like a ham radio installation, which matters if you rent. It is what I use on indoor room servers near a window and on the box of a small repeater where a 26-inch fiberglass stick would be in the way.

You will need an N-female to SMA-male adapter to connect it to a board.

## On a roof or mast: 5.8 dBi fiberglass

The fiberglass omni is the standard fixed-node antenna for a reason: it is sealed, it survives weather, and it has a proper N connector. The listing in the box comes with a mounting bracket and a length of cable; check the cable's connectors before you order, because you may still need an adapter at the board end.

Two things about the gain number. First, "5.8 dBi" on a fiberglass omni is achieved by squashing the pattern flat, so the antenna hears well out to the horizon and poorly up or down. Mount it vertical and level. Second, a longer, higher-gain stick is not automatically better; on a hill, a flatter pattern can shoot right over the town below you. The 5.8 dBi size is the safe choice for most rooftops.

## The mistakes that waste the money

**Buying by gain.** Height and a clear line of sight beat a few decibels of antenna gain every time. A 3 dBi antenna on the roof outperforms a 10 dBi antenna in the attic.

**RP-SMA.** Wi-Fi antennas use reverse-polarity SMA, which looks the same and does not mate. Every MeshCore board I own is standard SMA. If an antenna listing says RP-SMA, it is for a router.

**Wrong band.** 868 MHz antennas are everywhere because Europe uses that band. They will "work" at 915 with worse match and shorter range. Buy 902 to 928 MHz, U.S., 915.

**Long cheap coax.** RG174 and RG58 lose a lot at 915 MHz. If the antenna is more than a few feet from the board, use LMR-400 or shorten the run. Better yet, put the board in a box at the antenna.

**Transmitting with no antenna.** Powering a board with nothing on the SMA connector can damage the radio, especially on the higher-power boards. Antenna on first, always.

**Trusting the number on the listing.** Amazon antenna listings claim whatever they want. Judge an antenna by the RSSI and SNR you see from a known repeater before and after you swap it, not by the dBi in the title.

## What to check after you swap

Open the MeshCore app, find a repeater you can hear, and note the RSSI and SNR on a few messages or a trace. Change the antenna, same spot, same orientation, same repeater, and compare. If the numbers did not move, the antenna was not the limit; the location was. Move the radio before you buy another antenna.
