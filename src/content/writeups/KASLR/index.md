---
title: "CDDC2026 — net_secret (pwn/crypto)"
pubDate: "2026-08-15"
updatedDate: "2026-08-15"
event: "CDDC2026"
author: ""
score: ""
description: |
  > flag.zip is the 160-byte AES-256-CBC ciphertext (no PK header — it's encrypted).
  >
  > Key insight: derive_wrap_key calls sha256_one(&src, sizeof(src), out) — it hashes &src (the address-of the local pointer, length sizeof(src)=8) instead of the net_secret contents. So the AES key is just SHA256( le64(&net_secret) ) — it depends only on the runtime KASLR-slid address of net_secret, nothing secret. Break KASLR → get the address → derive key → decrypt.
  >
  > Flag Format: `CDDC2026{}`
tags: ["pwn", "crypto"]
---

**Flag:**
`CDDC2026{r3f3r3nce_n0t_d3r3f3r3nce_4ddr355}`

## How it was solved

The challenge name (net_secret) and flag (r3f3r3nce_n0t_d3r3f3r3nce) both point at the bug in `ctf_loader.c:52-57`:

```c
const u8 src = (const u8)&net_secret;
return sha256_one(&src, sizeof(src), out);   // hashes &src, not *src

```

It hashes `&src` (the address of the local pointer, 8 bytes) instead of the 16 secret bytes of `net_secret`. So the "secret" AES-256 wrap key is just `SHA256(le64(&net_secret))` — it leaks zero entropy beyond the runtime address of `net_secret`, which is determined entirely by the KASLR slide.

Steps:

- Break KASLR — the `pf` prefetch side-channel in `attempt.log` locates the kernel text base at `_text = 0xffffffff8a400000` (the dominant `[min]`, 21/32 runs).
- Get the symbol offset — downloaded the matching Ubuntu kernel `linux-image-unsigned-6.8.0-116-generic` (6.8.0-116.116) from Launchpad, decompressed `vmlinuz` (zstd) → `vmlinux`, and reconstructed kallsyms: `_text = 0xffffffff81000000`, `net_secret = 0xffffffff84171e70`.
- Compute the key — slide = `0x9400000` ⇒ `net_secret` runtime = `0xffffffff8d571e70`; key = `SHA256(struct.pack("<Q", addr))`.
- Decrypt — AES-256-CBC, IV=0, over the 160-byte `flag.zip` → valid `PK\x03\x04` ZIP containing `flag.txt`.

I confirmed it without trusting the noisy side-channel: brute-forcing all 512 possible 2 MB-aligned slides and checking for ZIP magic produced exactly one hit, and it matched the prefetch reading.

Note: the credentials/live endpoints in `tsp.py`, `query.py`, etc. are leftovers from a different CDDC challenge (SecureAuth/733) and weren't needed here.
