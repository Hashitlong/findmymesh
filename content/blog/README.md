# How to write a post

One file per post in this folder, named like `heltec-v3-vs-v4.md`. Top of the file is a short header, then the article in plain Markdown.

```
---
title: Heltec V3 vs V4: which should you buy for MeshCore?
date: 2026-11-02
summary: I've run both on my roof for months. Here's where the V4 earns its extra money and where it doesn't.
category: Comparisons        (Comparisons | Reviews | Builds | How-to)
hero: heltec-v3-v4.jpg       (optional; put the photo in content/images/)
products:
  - name: Heltec WiFi LoRa 32 V3
    amazon: https://www.amazon.com/dp/XXXXXXXX?tag=findmymesh-20
    verdict: Still the best cheap board. Fine as a companion, OK as a repeater.
    owned_since: 2025-08
  - name: Heltec WiFi LoRa 32 V4
    amazon: https://www.amazon.com/dp/XXXXXXXX?tag=findmymesh-20
    verdict: Worth it for a repeater. Better receiver, protected screen.
    owned_since: 2026-03
---

Write the article here. Photos: ![caption](photo-name.jpg) using files in content/images/.
Headings with ## work. Lists work. Keep it in your own words; the site handles the Amazon disclosure.
```

Rules the site enforces automatically:
- The Amazon disclosure sentence is added at the top and bottom of every post that lists products.
- Every Amazon button is labeled "Paid link" and only appears if the link carries your tag (`tag=`).
- No prices on the page (Amazon only allows those through its API).
