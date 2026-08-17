---
title: "LA CTF — lactf-1986 (rev)"
pubDate: "2026-08-15"
updatedDate: "2026-08-15"
event: "LA CTF"
author: ""
score: ""
description: |
  > Dug around the archives and found a floppy disk containing a long-forgotten LA CTF challenge. Perhaps you may be the first to solve it in decades.
  >
  > Flag Format: `lactf{}`
tags: ["rev"]
---

- **Challenge:** lactf-1986
- **Category:** Reverse Engineering
- **Points:**
- **Flag:** `lactf{...}`

---


This document is a step-by-step guide for solving the challenge using Ghidra. Follow in order; use the checkboxes to track progress.

---

## Part 3: Flag validation and how to get the flag

This section summarizes what the core validation function does and gives a concrete sequence to recover the flag.

### 3.1 Where the check happens

The main flag-checking logic lives in **FUN_1000_00b0** (and any functions it calls). The success path that writes the flag to a file is **FUN_1000_04e1** (opens file for write, writes twice, then **FUN_1000_08f1**, then exit).

### 3.2 What FUN_1000_00b0 does

1. **Copy 73 bytes from the binary into a local buffer**
   At **1000:00c6** `MOV CX, 0x24` (36), then **1000:00d0** `MOV SI, 0x146`, **1000:00d3** `REP MOVSW` (36 words = 72 bytes), then **1000:00d5** `MOVSB` (1 byte). So **73 bytes** are copied from DS:**0x146** into **local_a0**. This is the **target** (expected XOR result).

2. **Read user input into local_ea**
   Helper functions (e.g. **FUN_1000_021f**, **FUN_1000_027e**) fill **local_ea** with the user's input (from file or keyboard); **1000:0101** null-terminates at the read length. So **local_ea** is the **input buffer**.

3. **Check the prefix "lactf{"**
   The code compares (listing): `local_ea[0]==0x6c` ('l'), `local_e9==0x61` ('a'), `local_e8==0x63` ('c'), `local_e7==0x74` ('t'), `local_e6==0x66` ('f'), `local_e5==0x7b` ('{'). So the required prefix is **`lactf{`**.

4. **Initial state for the key stream**
   **1000:0164–0167** `LEA AX, local_ea` then `CALL FUN_1000_0010`. **1000:016a–016d** store the result (AX, DX) at **0x346** and **0x348**. So the key stream is seeded by **FUN_1000_0010(pointer to input)** — a hash of the null-terminated input. The loop index at **0x144** is set to 0.

5. **XOR check (main validation)**
   For each index **i** from 0 to 72 (loop runs while **SI < 0x49**, i.e. 73 iterations):
   - **1000:0182–0185** Load state from **[0x346]** and **[0x348]** (AX, DX).
   - **1000:0189** `CALL FUN_1000_007b` → new state in AX, DX.
   - **1000:018c–018f** Store new state at 0x346, 0x348.
   - **1000:019d** **key_byte** = low byte of **new** state = `[0x346]` (AL).
   - **1000:01a0** `AL ^= input[i]`.
   - **1000:01a6** `CMP AL, local_a0[i]` — requires **key_byte ^ input[i] == target[i]**.

   So the **correct** input byte at position **i** is:
   **input[i] = key_stream[i] ^ target[i]**,
   where **target** = 73 bytes at DS:**0x146** (1239:0146–018e), and **key_stream[i]** = low byte of the state at 0x346 **after** the i‑th call to **FUN_1000_007b()**.

### 3.3 Summary formula

- **Flag format:** `lactf{` + 73 bytes of checked input (bytes 0..72). Trim at first `}` or null for the actual flag string.
- **For i = 0..72:**
  **input[i] = key_stream[i] ^ target[i]**
  - **target[i]** = byte at **1239:0146 + i** (73 bytes: 1239:0146 through 1239:018e).
  - **key_stream[i]** = low byte of state at 0x346 **after** the i‑th call to **FUN_1000_007b()**.
- **Initial state** (before any call) = **FUN_1000_0010**(pointer to input), so the key stream depends on the full input (see “How to proceed” below).

### 3.4 Step-by-step: how to get the flag

- [ ] **Step A: Dump the 73-byte target from the binary**
      In Ghidra go to **0x1239:0146** (or linear **0x124d6**). Copy **73 bytes** (1239:0146 through 1239:018e) → **target[0..72]**.

- [ ] **Step B: Obtain the key stream (73 bytes from FUN_1000_007b)**
  - **Option B1:** Reimplement **FUN_1000_0010** and **FUN_1000_007b** (see “How to proceed” below), compute initial state then 73 key bytes.
  - **Option B2:** Run the binary in DOS, break after each **FUN_1000_007b** call in the loop, and record the byte at 0x346, 73 times (input must pass the "lactf{" check so the loop runs).

- [ ] **Step C: Compute the flag bytes**
      For **i = 0..72**: **flag_byte[i] = key_stream[i] ^ target[i]**.

- [ ] **Step D: Build the flag**
      **flag = "lactf{" + the 73 computed bytes (as characters).** Stop at the first `}` or null for the shortest flag.

- [ ] **Step E: Submit**
      The result is **lactf{...}**.

### 3.5 Optional: confirm the success path

**FUN_1000_04e1** runs on success: opens a file for writing, performs two writes (likely the flag or success message), calls **FUN_1000_08f1**, then exits. Tracing the data passed to those writes can confirm the computed flag.

---

# LaCTF 1986 (DOS binary) — progress

Summary of what we did so far on the **lactf-1986** challenge (CHALL.EXE, 16-bit DOS).

## Setup and entry (Ghidra)

- Loaded **CHALL.EXE** in Ghidra (x86 16-bit, real-mode).
- **entry** parses the command line from the PSP (0x80/0x81), opens a file (first argument), and parses env/switch for **ON78** vs **FLN** (mode flags).
- Labeled/annotated INT 21h calls (e.g. dos_open_file, dos_get_version, dos_open_file_write, write, exit) and key labels (e.g. parse_ON78).

## Key functions

- **FUN_1000_04e1** — success path: opens a file for writing, does two writes (flag/message), calls **FUN_1000_08f1**, then exit.
- **FUN_1000_00b0** — core flag validation (see below).

## Flag validation (FUN_1000_00b0)

1. **73-byte target** copied from the binary (36 words + 1 byte from DS:0x146) into **local_a0**.
2. User input is read into **local_ea** (from file/keyboard via helpers); null-terminated at read length.
3. **Prefix check:** first 6 bytes must be **`lactf{`**.
4. **Initial state:** **FUN_1000_0010**(pointer to input) → (AX, DX) stored at 0x346, 0x348.
5. **XOR check:** for `i = 0..72` (loop while SI < 0x49), the program calls **FUN_1000_007b()**, then uses the **low byte of the new state** at **0x346** as key_byte, and requires
   **key_byte ^ input[i] == target[i]**
   So: **correct input[i] = key_stream[i] ^ target[i]**.

**Formula:**
`flag = "lactf{" + (key_stream[i] ^ target[i]) for i in 0..72`

- **target** = 73 bytes at **1239:0146–018e**.
- **key_stream[i]** = low byte at 0x346 **after** the i-th call to **FUN_1000_007b()**.

## Finding the right address for the 73-byte target

The code copies 73 bytes (36 words + 1 byte) from address **0x146**, but in 16-bit DOS that is an **offset**; the **segment** is implied (usually DS). Here’s how we found the correct segment.

1. **Use the listing for FUN_1000_00b0**
   At the top it says **`assume CS = 0x1000`**, so we first assumed the data might be in the same segment.

2. **Go To 0x1000:0146 (or linear 0x10146)**
   In Ghidra: **Navigation → Go To** and enter **0x10146** or **1000:0146**.

3. **What we saw there**
   The Listing showed **code**, not data:
   - `1000:0145  MOV AX, 0x1`
   - `1000:0148  JMP LAB_1000_014c`
     So 0x146 in segment **0x1000** is in the middle of a `MOV` instruction, not the target table.

4. **Conclusion**
   The offset **0x146** is used with the **data segment (DS)**, not the code segment (CS). Other globals in the decompilation are named like **DAT_1239_02b4** — the **0x1239** is the segment for that data.

5. **Try the data segment 0x1239**
   **Go To** → **0x1239:0146** (or linear **0x124d6** = 0x1239×16 + 0x146).

6. **Result**
   At **1239:0146** we see raw bytes (e.g. `b6 8c 95 8f ...`) with no instruction pattern. The 73-byte target runs from **1239:0146** through **1239:018e** (inclusive).

So: **0x146** in the source means **DS:0x146**; in this binary **DS = 0x1239** for that data, so the target is at **1239:0146**.

## Step A done: target bytes

The 73-byte target at **1239:0146–018e** was dumped. Use this in the XOR step:

```python
target = [
    0xb6, 0x8c, 0x95, 0x8f, 0x9b, 0x85, 0x4c, 0x5e,
    0xec, 0xb6, 0xb8, 0xc0, 0x97, 0x93, 0x0b, 0x58,
    0x77, 0x50, 0xb0, 0x2c, 0x7e, 0x28, 0x7a, 0xf1,
    0xb6, 0x04, 0xef, 0xbe, 0x5c, 0x44, 0x78, 0xe8,
    0x99, 0x81, 0x04, 0x8f, 0x03, 0x40, 0xa7, 0x3f,
    0xfa, 0xb7, 0x08, 0x01, 0x63, 0x52, 0xe3, 0xad,
    0xd1, 0x85, 0x9f, 0x94, 0x21, 0xd5, 0x2a, 0x5c,
    0x20, 0xd4, 0x31, 0x12, 0xce, 0xaa, 0x16, 0xc7,
    0xad, 0xdf, 0x29, 0x5d, 0x72, 0xfc, 0x24, 0x90,
    0x2c
]

```

## Next: Step B (key stream)

- Get 73 bytes from **FUN_1000_007b()** (reimplement **FUN_1000_0010** and **FUN_1000_007b**, or run in DOS and record the byte at 0x346 after each of the 73 calls).
- **FUN_1000_007b** does not use the string at 1239:0116 or the bit table at 1239:013c; it only uses the 32-bit state (AX,DX) and implements an LFSR-style update (shift right 3, feedback bit, then 1 more shift, mask DX to 4 bits).
- Then: `flag = "lactf{" + "".join(chr(key_stream[i] ^ target[i]) for i in range(73))` (trim at `}` or null).

---

## How to proceed (detailed)

The key stream depends on the **initial state** from **FUN_1000_0010(pointer to input)**. That function hashes the **entire** null-terminated input, so the state is a function of the full flag — which we don’t know yet. You can proceed in one of these ways.

### Option 1: Reimplement and try initial state from prefix only

1. **Reimplement FUN_1000_0010** (from the listing ~1000:0010–0070):
   - It takes a pointer (AX) to a null-terminated string.
   - It maintains a 20-bit state: low 16 bits in a word, high 4 bits in SI. For each byte `c` until `\0`: state is updated like `state = (state << 6) + (state << 1) + c` (with 20-bit wrap). Return (AX, DX) = that state (AX = low word, DX high part masked to 4 bits).
   - Implement this in Python (or C), and compute `init_state = fun_1000_0010(b"lactf{")` (or `"lactf{"` with a null if your impl expects it).

2. **Reimplement FUN_1000_007b** (from the listing ~1000:007b–00ae):
   - Input: (AX, DX) = 32-bit state (DX only uses low 4 bits effectively).
   - Logic: (BX, SI) = (AX, DX). Rotate (AX, DX) right by 3 bits. DI = (AX ^ BX) & 1 (feedback). Rotate (AX, DX) right by 1 more. Put feedback into high nibble of DX; DX &= 0xf. Return (AX, DX) as new state. The **key byte** used by the checker is the **low byte of this new state** (AL).
   - Implement `next_state(ax, dx) -> (new_ax, new_dx)` and `key_byte = new_ax & 0xff`.

3. **Compute key stream and flag:**
   - If you assume the initial state is from hashing only `"lactf{"` (input truncated at 6 bytes), then:
     - `state = fun_1000_0010(b"lactf{")` (or plus `\0` depending on your impl).
     - For i in 0..72: `(state_ax, state_dx) = fun_1000_007b(state_ax, state_dx)`; `key_stream[i] = state_ax & 0xff`; update state.
     - `flag_bytes[i] = key_stream[i] ^ target[i]`.
     - `flag = b"lactf{" + bytes(flag_bytes)`; trim at `}` or null.
   - Check: if the result looks like readable text and ends with `}`, you’re done. If not, the initial state may depend on more of the input (see Option 2).

### Option 2: Fixed-point (if Option 1 doesn’t yield a valid flag)

The initial state is `hash(full_input)`. So we need **input** such that:

- `input = b"lactf{" + (key_stream ^ target)[0:67]` (or 73 bytes then trim),
- and `hash(input)` equals the state used to generate that **key_stream**.

You can try iterating: start with a candidate (e.g. from Option 1), compute `state = hash(candidate)`, generate key stream from that state, compute new candidate = `"lactf{" + (key_stream ^ target)`, and repeat until `candidate` stabilizes or you get a consistent flag.

### Option 3: DOS / debugger

Run **CHALL.EXE** in DOS (or DOSBox) with an input that starts with `lactf{` (e.g. from a file). Attach a debugger, set a breakpoint after each **FUN_1000_007b** return (e.g. at 1000:018c), and each time record the byte at **0x346** (in the correct segment). Do this 73 times to get **key_stream[0..72]**. Then `flag = "lactf{" + bytes(key_stream[i] ^ target[i] for i in range(73))` (trim at `}`).

### Summary

- **Target:** 73 bytes in the listing at **1239:0146–018e** (already listed in “Step A done” above).
- **Key stream:** 73 bytes = low byte of state at 0x346 after each of 73 calls to **FUN_1000_007b**, with initial state from **FUN_1000_0010**(input).
- **Flag:** `lactf{` + `(key_stream[i] ^ target[i]) for i in range(73)`; trim at first `}` or null.
