---
title: Heltec V3 vs V4 for MeshCore: what the extra money buys
date: 2026-11-07
summary: The V4 is the same board with a better radio, a protected screen and a solar input. Whether that is worth it depends entirely on what you're plugging it into.
category: Comparisons
products:
  - name: Heltec WiFi LoRa 32 V3
    amazon: https://www.amazon.com/dp/B0D1H1FN9Y?tag=findmymesh-20
    verdict: Still the right first board. Companion, bench repeater, room server on USB power.
  - name: Heltec WiFi LoRa 32 V4
    amazon: https://www.amazon.com/dp/B0FS1R4HXH?tag=findmymesh-20
    verdict: Worth it for a mains-powered repeater where you want the stronger transmitter.
---

The Heltec V3 is the board most people start MeshCore on. The V4 came out as a drop-in replacement: same footprint, same pinout, same ESP32-S3 and SX1262 family, with a few targeted changes. I have run both in the same spots, so this is a short one.

## What is the same

- ESP32-S3 microcontroller, so the power draw story is the same: fine on USB, poor on a small battery. Neither is a solar repeater board.
- SX1262-class LoRa radio, 902 to 928 MHz variant for the U.S.
- 0.96-inch OLED, SMA antenna connector, USB-C.
- Both are in the official MeshCore flasher as companion, repeater and room server.

## What the V4 changes

**Transmit power.** The V3's SX1262 tops out at about 22 dBm (roughly 160 mW). The V4 adds a power amplifier; Heltec's page lists a high-power version at 28 dBm and the Amazon listing says 27 dBm. Call it four times the transmit power. That helps you be heard; it does nothing for how well you hear, and on a mesh, hearing is usually the limit.

**Protected screen.** The V3's OLED is glued on top of the board and is the first thing to break. The V4's is recessed and covered. Small thing, matters in a bag.

**Solar input.** The V4 has a second 1.25 mm connector for a 4.7 to 6 V solar panel, next to the battery connector. That sounds like it makes a solar repeater; it doesn't really, because the ESP32 idle draw is still high. It makes a battery-backed repeater that can top itself up in good sun.

**GNSS header.** The V4 has an 8-pin connector for an optional GPS module. The V3 has no GPS option without wiring one yourself.

## Which one, for what

**Companion in a case, paired to your phone:** V3. The extra transmit power does not help much in a pocket, and the price difference buys a better antenna.

**Room server or repeater sitting on a shelf on USB power:** V4. You are plugged in, so the power draw doesn't matter, and the stronger transmitter helps your messages reach a repeater that is at the edge.

**Solar or battery repeater on a roof:** neither. Buy an nRF52 board (RAK4631, Heltec T114, Seeed XIAO nRF52840) or a finished solar node. I wrote up the reasoning in the repeater board comparison.

**Learning and bench work:** V3, and buy two. They are cheap enough that one can stay a test repeater forever.

## One warning about antennas

Both boards will transmit into a bad antenna or no antenna. On the V4 especially, with the amplifier, powering it up with nothing on the SMA connector is a good way to damage the radio. Antenna first, power second, always.

## Further reading

Our sister site Prepped Gear has a [Heltec V3 vs V4 comparison](https://preppedgear.com/heltec-v3-vs-v4/) written from the Meshtastic side, including the GNSS version of the V4 and a two-pack kit, if you run both firmwares.
