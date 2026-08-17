---
title: "image-progress (for)"
pubDate: "2026-03-21"
updatedDate: "2026-03-21"
event: "bsides-ctf"
author: "slacksleepsloth"
score: ""
description: |
  > Chrome is re-adding JPEG XL support to help the web PROGRESS, so we thought a SALIENT challenge was in ORDER!
tags: ["for"]
---

[https://opensource.googleblog.com/2021/09/using-saliency-in-progressive-jpeg-xl-images.html](https://opensource.googleblog.com/2021/09/using-saliency-in-progressive-jpeg-xl-images.html)

Google Open Source Blog
Using Saliency in progressive JPEG XL images
At Google, we are working towards improving the web experience for users. Getting images delivered fast is a crucial part of the web experience and

Image [https://github.com/libjxl/libjxl](https://github.com/libjxl/libjxl)

GitHub - libjxl/libjxl: JPEG XL image format reference implementation
JPEG XL image format reference implementation. Contribute to libjxl/libjxl development by creating an account on GitHub.
ill prob continue solving this frm Tues onwards ._.
But i think its to do with how JXL orders the display

It typically orders it in 256x256 grids which fits the ASCII table in the image (16 characters across)

my guess is the order will output the flag with the ASCII characters

I built the image layer by layer and use arrow keys to see what letters were highlighted

![Before. Screenshot](before.png)

![After. Screenshot](after.png)
