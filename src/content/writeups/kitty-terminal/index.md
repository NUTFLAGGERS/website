---
title: "bsides-ctf — kitty-terminal (term)"
pubDate: "2026-03-21"
updatedDate: "2026-03-21"
event: "bsides-ctf"
author: "mae"
score: ""
description: |
  > I hide and only come out for certain terminals, can you find me?
  > Flag Path: /home/ctf/flag.kitty
  > Author: symmetric
  > Web Terminal: https://kitty-7c6c7969.term.challenges.bsidessf.net (or socat STDIO,raw,echo=0,escape=0x03 TCP:kitty-7c6c7969.challenges.bsidessf.net:8024)
  > https://kitty-7c6c7969.term.challenges.bsidessf.net
tags: ["term"]
---

# kitty-terminal — bsides-ctf (term)

—
[https://github.com/kovidgoyal/kitty](https://github.com/kovidgoyal/kitty)

If you base64 it you get this whole chunk

![image.png](./image.png)

hint: it takes a kitty to see a kitty
normal cat didnt work so i installed the kitty terminal and ran the command given in the challenge description, then cat as normal

**Note:** i think theres another way to solve this without setting up the kitty terminal, if you can somehow convert the base64 data inside flag.kitty into an image and open it
