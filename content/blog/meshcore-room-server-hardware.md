---
title: Running a MeshCore room server: what it is and what to put it on
date: 2026-11-16
summary: A room server is a bulletin board for your mesh. It needs power, a decent spot, and almost nothing else. The boards you already have are fine.
category: How-to
products:
  - name: Heltec WiFi LoRa 32 V4
    amazon: https://www.amazon.com/dp/B0FS1R4HXH?tag=findmymesh-20
    verdict: My pick for a plugged-in room server. Loud radio, protected screen.
  - name: Heltec WiFi LoRa 32 V3
    amazon: https://www.amazon.com/dp/B0D1H1FN9Y?tag=findmymesh-20
    verdict: The board you already own. Perfectly good on USB power.
  - name: ALFA AOA-915-5ACM 5 dBi outdoor antenna
    amazon: https://www.amazon.com/dp/B08H8J6ZV6?tag=findmymesh-20
    verdict: A short outdoor antenna for a room server near a window.
  - name: SMA to N adapter kit (4 pack)
    amazon: https://www.amazon.com/dp/B06XPDWBPR?tag=findmymesh-20
    verdict: For the ALFA's N connector.
---

MeshCore has three firmware roles: companion (the radio you carry), repeater (relays traffic), and room server. The room server is the one people skip, and it is the one that makes a small mesh feel like a community instead of a walkie-talkie.

## What a room server does

A room server stores posts like a small bulletin board, so people can read messages they missed. Companions only hear what is sent while they are on; if your radio was off or out of range, that message is gone. A room server keeps it. Users join the room from the app, read the backlog, and post to it.

A room server can also have repeat turned on, in which case it relays like a repeater. Off by default; leave it off unless the room server is the only thing in a spot that needs a repeater anyway.

## What it needs

Power, mostly. A room server sits still, so battery life does not matter and ESP32 boards are fine. It needs to be where your companions can reach it, directly or through a repeater, so near a window beats a basement. And it needs an antenna that is not the stock stub.

## Boards

**Heltec V4.** My pick. It is a plugged-in board anyway, the amplified radio (27 to 28 dBm) helps it be heard, and the recessed screen survives a shelf. The V4 is in the flasher as a room server.

**Heltec V3.** If you started on one and bought a better companion, this is where the V3 goes. Same flash procedure, same USB power.

**Anything nRF52 you have spare.** The T114, RAK4631 and XIAO kits all have room server builds in the flasher. They are overkill for a mains-powered box, but a spare is a spare.

## Antenna

A room server near a window does well on a short outdoor antenna like the ALFA 5 dBi, which is weatherproof and inconspicuous on a windowsill or a balcony rail. It has an N connector, so you need an N-female to SMA-male adapter. Indoors, the 17 cm whip from the companion articles is fine.

## Setting it up

1. Flash the Room Server role at flasher.meshcore.io over USB.
2. Configure over USB at config.meshcore.io: name, U.S. radio settings (same as your repeaters), location if you want it on the map, and an admin password.
3. Reboot after the radio settings change; they take effect on restart.
4. From a companion, send an advert and confirm the room shows up, then join it and post a test.
5. Write the admin password down somewhere that is not the room server.

## Name it like a place

Repeaters get named for where they are. Room servers get named for what they are for: "Lake Norman general," "Cornelius trade," "Weather." People will find them by name in the app, and a clear name means fewer "what is this room" questions in the group chat.
