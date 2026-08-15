---
title: "PNGception — Steg in Steg"
pubDate: "2025-04-21"
event: "Grey Cat The Flag 2025"
author: "0xCat"
score: "250 pts"
tags: ["misc"]
description: "Multi-layered PNG chunk steganography and LSB bit plane extraction."
---

# PNGception (Misc - 250 pts)

## Challenge Analysis
An image `inception.png` was provided. Standard inspection revealed nested custom PNG chunks and hidden least-significant bit data.

## Step-by-Step Solution

1. **Extracting Custom PNG Chunks**:
   Using `pngcheck`:
   ```bash
   pngcheck -v inception.png
   ```
   We observed non-standard `zTXt` and `tRNS` chunks containing base64 encoded strings.

2. **LSB Bit-plane Extraction**:
   Using Python PIL to extract lower bits:
   ```python
   from PIL import Image

   img = Image.open("inception.png")
   pixels = img.load()
   bits = ""
   for y in range(img.height):
       for x in range(img.width):
           r, g, b, a = pixels[x, y]
           bits += str(a & 1)

   bytes_list = [int(bits[i:i+8], 2) for i in range(0, len(bits), 8)]
   print(bytes(bytes_list).decode('latin1'))
   ```

Flag: `grey{st3g_w1th1n_st3g_1nc3pt10n_31337}`.
