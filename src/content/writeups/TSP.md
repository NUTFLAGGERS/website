---
title: "CDDC2026 — Temporal Serialization Protocol (misc)"
pubDate: "2026-08-15"
updatedDate: "2026-08-15"
event: "CDDC2026"
author: ""
score: ""
description: |
  > A system log shows time being serialized into a strict sequence.
  > Through time serialization, paths that should not align begin to overlap.
  > If the ordering is manipulated correctly, something unreachable may become reachable.
  > Try it before the sequence resets.
  >
  > https://cddc2026.xyz:5007/
  > Flag Format: `CDDC2026{}`
tags: ["misc"]
---

❗ AI Used!

**Flag:**
`CDDC2026{T1me_Str3ngth3ns_p07en7ial_4nd_4w4kens_Purp0se}`

## How it worked

The challenge (https://cddc2026.xyz:5007/) was an insecure deserialization bug in a custom binary protocol (TSP — Temporal Serialization Protocol), not a classic LFI.

Reversed the protocol — 12-byte header (magic 0xC4E71A59, version 0x21), type-tagged values, custom varint, and XOR-encoded strings. I recovered the 4-byte XOR key ("gate", reset per-string) by brute-forcing the `/api/temporal/status` response against English-letter frequency.

Found the gadget — a normal `TemporalQuery` reply contained a `_next` field with an undocumented tag `0xe7` = a handler-invocation object: `[0xe7][handler name][args list]`. The engine exposed handlers `read_temporal_data`, `encode_data`, `echo`, `concat`, etc.

Achieved arbitrary file read — placing a `0xe7` call as a parameter value got the server to execute it. `read_temporal_data("/etc/passwd")` dumped the file (relative `../` traversal was blocked, but absolute paths weren't).

Bypassed the output filter — `/flag.txt` existed but was blocked ("apply a layer of transforms"). The gadget supports nesting calls as arguments, so I chained `encode_data(read_temporal_data("/flag.txt"))` → base64, defeating the content filter → decoded to the flag.

The hint maps cleanly: "time serialization" = TSP, "paths that should not align begin to overlap" = the call-injection giving file access, and "reshape the fragment into a stable form" = the `encode_data` transform.

The exploit scripts are as attached below (`tsp.py`, `query.py`, `read.py`):

### ❗ `tsp.py` — the protocol codec (foundation)

The library that speaks the custom Temporal Serialization Protocol. Everything else imports it. It holds:

- VarInt encode/decode (the custom big-endian, continuation-bit-0 variant).
- String XOR with the recovered key "gate" (`enc_str`/`decode`), plus the type-tag encoders (`enc_int32`, `enc_map`, `enc_obj`, `enc_tcoord`, and crucially `enc_call` for the `0xe7` handler-invocation gadget).
- A recursive `decode()` that turns a raw TSP response back into a Python dict — including the `0xe7` call type I reverse-engineered.
- `collect_strings()` — the helper I used to scrape ciphertext out of the status blob to brute-force the XOR key.

In short: read and write TSP bytes. No network here.

### `query.py` — the transport + request builder

Wraps `tsp.py` into actual HTTP requests:

- `checksum()` + `frame()` — bolt on the 12-byte header (magic, version, flags, length, checksum) so the server accepts the payload.
- `build_query()` — assembles a valid TemporalQuery object (timestamp + parameters map) where I can drop arbitrary parameter values.
- `send_raw()` — POSTs to `/api/temporal/compute` via curl, splits headers/body, and decodes the TSP response.
- `show()` — pretty-prints whatever comes back.

In short: build a well-formed request and send it. This is what I ran to get the first baseline response that exposed the handler list and the `_next` gadget.

### `read.py` — the weaponized exploit

The thin payload script that uses the other two to actually extract files. It sets the dimension parameter to a `0xe7` call → `read_temporal_data(<path>)`, and prints the returned dimension field. I used it to:

- fuzz filenames / path-traversal,
- confirm arbitrary file read (`/etc/passwd`),
- and locate `/flag.txt`.

In short: the file-read primitive. (The final base64-bypass — `encode_data(read_temporal_data("/flag.txt"))` — I ran as an inline one-liner rather than adding it to `read.py`.)

So the dependency chain is: `read.py` → `query.py` → `tsp.py`. Codec at the bottom, transport in the middle, exploit on top. The other files (`brute.py` recovered the XOR key; `send.py`/`x.py` were scratch probes) were throwaways along the way.
