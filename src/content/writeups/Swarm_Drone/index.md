---
title: "CDDC2026 — Swarm Drone (protocol)"
pubDate: "2026-08-15"
updatedDate: "2026-08-15"
event: "CDDC2026"
author: ""
score: "350"
description: |
  > A drone swarm flew a coordinated mission over our airspace. We captured the
  > full **MAVLink** link between the swarm and the Ground Control Station (GCS).
  >
  > During the operation an adversary **flooded the same link with FORGED telemetry**,
  > impersonating our drones to poison the picture.
  >
  > **Recover what our real drones were actually doing.**
  >
  > Flag Format: `CDDC2026{}`
tags: ["protocol"]
---

# Swarm Drone — CDDC2026 (Protocol, 350 pts)

**Flag:** `CDDC2026{TRUST_TH3_K3Y_AND_V3R1FY_S1GNS}`

---

## 1. Challenge description & the hints in it

> A drone swarm flew a coordinated mission over our airspace. We captured the
> full **MAVLink** link between the swarm and the Ground Control Station (GCS).
>
> During the operation an adversary **flooded the same link with FORGED telemetry**,
> impersonating our drones to poison the picture.
>
> **Recover what our real drones were actually doing.**

Reading the description literally hands you the whole approach:

| Phrase in the description                                                          | What it tells you                                                                                                                                                                                                    |
| ---------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| "full **MAVLink** link"                                                            | The protocol is MAVLink (and the dist files confirm **MAVLink 2**).                                                                                                                                                  |
| "an adversary flooded ... with **FORGED** telemetry, **impersonating** our drones" | There is a mix of genuine and spoofed packets on the _same_ wire. We need a way to tell them apart that the attacker _cannot_ fake.                                                                                  |
| The dist ships a **`swarm.key`** alongside the capture                             | MAVLink 2 supports **packet signing** with a 32-byte shared secret. The key is given because the real drones sign their packets — the attacker, lacking the key, cannot produce a valid signature. This is the crux. |
| "Recover **what our real drones were actually doing**"                             | After filtering to the authentic packets, their telemetry (GPS) reconstructs the mission — which encodes the flag.                                                                                                   |

So the intended path is: **use the signing key to separate real from forged, then read the real mission.**

---

## 2. Files

```
chall.zip
└── chal/
    ├── capture.pcap   # 13,259 MAVLink 2 frames over UDP
    └── swarm.key      # 805d92604587c75923be28ba9535e242e002019c4bf88cd65b05b0efd25119c4  (32 bytes hex)
```

The pcap is a single UDP stream `192.168.1.10:14550 → 192.168.1.20:14550` (14550 is the canonical MAVLink/GCS port). **Every** payload begins with `0xFD` = the MAVLink **v2** start-of-frame magic.

---

## 3. MAVLink 2 background needed

**Frame layout (v2):**

```
+------+-----+-----------+-----------+-----+-------+--------+--------+---------+-----+-----------------+
| 0xFD | len | incompat  | compat    | seq | sysid | compid | msgid  | payload | CRC | signature(13B)  |
| 1    | 1   | 1         | 1         | 1   | 1     | 1      | 3      | len     | 2   | only if signed  |
+------+-----+-----------+-----------+-----+-------+--------+--------+---------+-----+-----------------+
```

- The **`incompat_flags`** field has bit 0 = `MAVLINK_IFLAG_SIGNED (0x01)`. When set, a **13-byte signature block** is appended: `link_id (1) || timestamp (6, LE, units of 10 µs) || signature (6)`.
- **Signature computation:**

  ```
  signature6 = SHA256( secret_key || full_frame_without_sig || link_id || timestamp )[:6]
  ```

  where `full_frame_without_sig` is the header + payload + 2-byte CRC (everything before the signature block).

- **Wire field ordering gotcha:** MAVLink serializes message fields **sorted by descending type size**, _not_ declaration order. So you must not hand-parse payloads by struct order — use a real dialect decoder (`pymavlink`). (My first hand-rolled `GPS_RAW_INT` parse produced garbage latitudes of ±200° precisely because of this.)

---

## 4. Solve steps

### Step 1 — Carve UDP payloads from the pcap

A tiny classic-pcap reader (no scapy needed): walk the 24-byte global header + per-record 16-byte headers, strip Ethernet(14)/IPv4/UDP(8), keep the payload. Result: 13,259 payloads, **all** starting with `0xFD`, all on the one stream.

### Step 2 — Verify every signature against `swarm.key`

For each frame: read `len` and `incompat_flags`, slice out the header+payload+CRC and the 13-byte trailer, then recompute the 6-byte signature and compare:

```python
data = frame_without_sig + link_id + timestamp        # bytes
expected = hashlib.sha256(KEY + data).digest()[:6]
valid = (expected == given_sig6)
```

Result:

```
total frames : 13259
valid (real) :  1958      <-- correct signature → authentic
invalid      : 11301      <-- forged flood, dropped
```

Every frame _claimed_ to be signed (`incompat=1`), but only 1,958 actually verify. The forged ~85% are discarded. The real packets are spread evenly across 20 drones (`sysid` 1–20).

### Step 3 — Decode the real telemetry

Feeding only the valid frames to `pymavlink` (`dialects.v20.common`):

```
valid msg types: GPS_RAW_INT × 1938,  HEARTBEAT × 20
```

The GPS fixes sit around **37.566 °N, 126.978 °E** (Seoul), alt 80 m — sane, coordinated positions. The forged ones (had we kept them) are noise.

### Step 4 — "What were the real drones doing?" → read the formation

Each drone's GPS track, **ordered by the signature timestamp** (the 6-byte field in the trailer, units of 10 µs), traces a path. Ordering the ~97 points per drone and connecting them draws a shape. Two refinements made it legible:

1. **Use the signature timestamp** for ordering, not pcap capture time (capture order is scrambled by the interleaved forged flood).
2. **Break the polyline on large jumps** — between glyph strokes the "pen" lifts and teleports; drawing those moves adds stray diagonals. Splitting a track wherever consecutive points jump more than a threshold removes them.

Each of the 20 drones then clearly draws **~2 ASCII characters**. Concatenating drones in `sysid` order 1→20:

```
sys1-5  :  C D D C 2 0 2 6 { T
sys6-10 :  R U S T _ T H 3 _ K
sys11-15:  3 Y _ A N D _ V 3 R
sys16-20:  1 F Y _ S 1 G N S }
```

→ **`CDDC2026{TRUST_TH3_K3Y_AND_V3R1FY_S1GNS}`** — "trust the key and verify signatures."

### Step 5 — Submit (platform quirk)

The CDDC `submit_flag` API expects the flag **base64-encoded** (the site's JS does `btoa(flag)` before POSTing). Sending the raw flag returns `"x"` (Incorrect) even when correct; base64-encoding it returns `"o"` (Correct).

---

## 5. Exploit / solver code

### a) pcap → MAVLink frames + signature verification

```python
import struct, hashlib
from collections import Counter, defaultdict

KEY = bytes.fromhex(open('swarm.key').read().strip())   # 32 bytes

def read_pcap(path):
    d = open(path, 'rb').read()
    endian = '<' if d[:4] == b'\xd4\xc3\xb2\xa1' else '>'
    off, pkts = 24, []
    while off + 16 <= len(d):
        _, _, incl, _ = struct.unpack(endian + 'IIII', d[off:off+16]); off += 16
        pkts.append(d[off:off+incl]); off += incl
    return pkts

def udp_payload(eth):                       # strip Eth/IPv4/UDP, return payload
    if len(eth) < 14 or struct.unpack('>H', eth[12:14])[0] != 0x0800: return None
    ip = eth[14:]; ihl = (ip[0] & 0x0f) * 4
    if ip[9] != 17: return None             # UDP only
    udp = ip[ihl:]; ulen = struct.unpack('>H', udp[4:6])[0]
    return udp[8:ulen]

frames = []
for eth in read_pcap('capture.pcap'):
    pl = udp_payload(eth)
    if not pl or pl[0] != 0xFD: continue
    length, incompat = pl[1], pl[2]
    signed = bool(incompat & 0x01)
    body = pl[:12 + length]                 # header + payload + CRC (pre-signature)
    sig  = pl[12 + length:12 + length + 13] if signed else b''
    frames.append(dict(sysid=pl[5], msgid=pl[7] | pl[8] << 8 | pl[9] << 16,
                       full=pl[:12 + length + (13 if signed else 0)],
                       body=body, sig=sig, signed=signed))

def verify(f):
    if not f['signed']: return None
    link_id, ts, given = f['sig'][0:1], f['sig'][1:7], f['sig'][7:13]
    return hashlib.sha256(KEY + f['body'] + link_id + ts).digest()[:6] == given

for f in frames: f['valid'] = verify(f)
print('valid', sum(f['valid'] for f in frames), '/ total', len(frames))
# -> valid 1958 / total 13259
```

### b) Real GPS tracks → render each drone's glyph

```python
import io
from collections import defaultdict
from pymavlink.dialects.v20 import common as mav
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt

mv = mav.MAVLink(io.BytesIO()); mv.robust_parsing = True
by = defaultdict(list)
for f in frames:
    if not f['valid']: continue
    m = mv.decode(bytearray(f['full']))
    if m.get_type() != 'GPS_RAW_INT': continue
    ts10us = int.from_bytes(f['sig'][1:7], 'little')        # signature timestamp = pen order
    by[f['sysid']].append((ts10us, m.lon, m.lat))

bx, byy = 1269780000, 375665000                              # origin offsets (deg*1e7)
def segments(seq, thresh=900):                               # split on pen-up jumps
    segs, px, py = [[]], None, None
    for _, x, y in seq:
        x -= bx; y -= byy
        if px is not None and abs(x-px) + abs(y-py) > thresh: segs.append([])
        segs[-1].append((x, y)); px, py = x, y
    return segs

fig, ax = plt.subplots(4, 5, figsize=(30, 22))
for i, s in enumerate(sorted(by)):
    a = ax[i//5][i%5]
    for seg in segments(sorted(by[s])):
        if seg: a.plot(*zip(*seg), 'k-', lw=2)
    a.set_title('sys%d' % s); a.set_aspect('equal'); a.axis('off')
plt.savefig('glyphs.png', dpi=75, bbox_inches='tight')
# Read drones sysid 1..20 left-to-right, top-to-bottom:
# CDDC2026{TRUST_TH3_K3Y_AND_V3R1FY_S1GNS}
```

### c) Submission (base64-encoded flag)

```python
import base64
flag = "CDDC2026{TRUST_TH3_K3Y_AND_V3R1FY_S1GNS}"
body = "i=753&f=" + base64.b64encode(flag.encode()).decode()
# POST body to  ./api/?c=submit_flag   ->  "o" (Correct)
```

---

## 6. Key takeaways

- **MAVLink 2 message signing is the authentication boundary.** With the shared `swarm.key` you recompute `SHA256(key || frame || link_id || timestamp)[:6]`; the attacker can flood the link but cannot forge a valid signature, so verification cleanly partitions real (1,958) from forged (11,301).
- **Order by the signature timestamp, not capture order** — the forged flood scrambles arrival order.
- **Decode with a real dialect parser** — MAVLink reorders fields by size on the wire; hand-parsing by declaration order yields nonsense.
- **The mission _is_ the message:** the authentic swarm flies a formation where each drone draws a couple of glyphs; concatenated in `sysid` order they spell the flag — which itself states the lesson: _trust the key and verify signatures._
- Platform quirk: the flag must be **base64** in the `submit_flag` API call.
