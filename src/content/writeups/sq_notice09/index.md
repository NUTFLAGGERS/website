---
title: "SQ_NOTICE09 (forensics)"
pubDate: "2026-09-17"
updatedDate: "2026-09-24"
event: "Singapore Cyber Conquest 2026 (SCC)"
author: "mae"
score: "1250"
description: |
  > Recover the clearance from the archived spool.
  > The capture is raw printer output. Anything that rewrites it as text, fixes its line endings or renders it will destroy part of the evidence and will not tell you it has.
tags: ["forensics", "printer"]
---

- **Challenge:** SQ_NOTICE09
- **Category:** Forensics
- **Author:** meyling
- **Flag:** `flag{n0t1c3_n1n3_jr_70b90f256d}`

---

## The Challenge

> Recover the clearance from the archived spool.
>
> The capture is raw printer output. Anything that rewrites it as text, fixes its line endings or renders it will destroy part of the evidence and will not tell you it has.

We're given four files:

- `NOTICE09.PRN` (698 bytes) — Raw printer spool output.
- `ROSTER.TXT` (307 bytes) — A shift roster table.
- `TEMPLATES.DOC` (4 KB) — A collection of stencils (masks with holes).
- `SEALED.BIN` (89 bytes) — Encrypted binary data where the flag is stored.

Right off the bat, the prompt gives a huge warning: **don't open and save `NOTICE09.PRN` in a regular text editor**. Any editor that "fixes" line endings or normalizes non-printable characters will strip out the exact bytes we need.

---

## 1. Checking NOTICE09.PRN

If we view `NOTICE09.PRN` (without resaving it), we see what looks like an old teletype log followed by a 12x12 grid of letters:

```text
@CONTINUITY WATCH LOEGF -- STATION P-0 -- PRINTER 2
AUTH SER 4471  WATCH 3  SHEET 1 OF 1
TRANSCRIEBFEEDF FROM TEEFLETYPE TAPE, NEOF CORRECTIONS APPLIED
RETEAFIN THIS SHEET WITH THE SHIFT REOFSTER
STENCIL FILED NEOFTHCH-UP.  THIESF SHEET PRINTS NOTECFH-RIGHT.
DO NOT REPRODUCE.  DESTROY AFTER RELIEF.
CIRCUIT CHECK COEMFPELFETED, NO FAULTS RECORDED THIS WATCH

BLOCK 9 -- 12 BY 12 -- APPLY STENCIL IN FORCE

RELAYKEWATCH
STANDINGBYNO
RTYHGATEQUIE
TSOUTIHGSATE
THQUIETPOWER
NOMINEAELLIN
EPRESSUMPRES
THEADAYSNOTR
AFIFSICRTHUI
SWANINPTCHRR
ELIEFIDUENAT
TTORWOTDEHRR

END BLOCK 9   SEAL CHK 4DA9EDC6
```

There are a few key details to pull from the header:
- `AUTH SER 4471`
- `WATCH 3`
- `BLOCK 9 -- 12 BY 12 -- APPLY STENCIL IN FORCE`
- `STENCIL FILED NEOFTHCH-UP. THIESF SHEET PRINTS NOTECFH-RIGHT.`
- Checksum at the bottom: `SEAL CHK 4DA9EDC6`

Also, notice all the weird typos in the words: `LOEGF`, `TRANSCRIEBFEEDF`, `TEEFLETYPE`, `NEOF`, `REOFSTER`, `COEMFPELFETED`... Keep that in the back of your mind.

---

## 2. Finding the Right Stencil

`ROSTER.TXT` is a simple lookup table:

```text
CONTINUITY SHIFT ROSTER -- CURRENT PERIOD
------------------------------------------------
WATCH 1   RELIEF 0600   CUT AUTHORITY 22
WATCH 2   RELIEF 1400   CUT AUTHORITY 30
WATCH 3   RELIEF 2230   CUT AUTHORITY 31
WATCH 4   RELIEF 0600   CUT AUTHORITY 20
------------------------------------------------
```

Since the header said `WATCH 3`, our cut authority is **31**.

Next, we open `TEMPLATES.DOC` and search for our serial (`SER 4471`) with a cut count of **31**. We find `SER 4471-J`:

```text
SER 4471-J    CUT COUNT 31

............##
...........##.
............#.
...#..#.....#
...####..#
#..........#..
#..#.#...##.
.........##..
...........#.#
..#.....##..#
....#..#....
....#.......
```

It's a 12x12 grid with holes (`#`), which matches our 12x12 letter block in `NOTICE09.PRN`.

---

## 3. Applying the Stencil

The note in `NOTICE09.PRN` tells us how to orient the stencil:
> `STENCIL FILED NOTCH-UP. THIS SHEET PRINTS NOTCH-RIGHT.`

The stencil is archived with the notch pointing **up**, but the sheet was printed with the notch pointing **right**. So we need to rotate the stencil **90° clockwise**:

```text
......##....
............
..#.........
....#..#....
##..........
.....#.#....
.......##...
.##....#....
..#.#..#..#.
..####...#.
.....#...#.#
..##...##..#
```

Now, overlay this rotated stencil on top of the 12x12 letter block:

```text
RELAYKEWATCH          ......##....          .....KE.....
STANDINGBYNO          ............          ............
RTYHGATEQUIE          ..#.........          ..Y.........
TSOUTIHGSATE          ....#..#....          ....I..S....
THQUIETPOWER    +     ##..........    =     TH..........
NOMINEAELLIN          .....#.#....          .....E.E....
EPRESSUMPRES          .......##...          .......MP...
THEADAYSNOTR          .##....#....          .HA....S....
AFIFSICRTHUI          ..#.#..#..#.          ..I.S..R..U.
SWANINPTCHRR          ..####...#.           ...NINP...R.
ELIEFIDUENAT          .....#...#.#          .....I...N.T
TTORWOTDEHRR          ..##...##..#          ..OR...DE..R
```

Reading the visible letters line by line:
`KE` `Y` `I S` `TH` `E E` `MP` `HA S` `I S R U` `NIN P R` `I N T` `OR DE R`

> **`KEY IS THE EMPHASIS RUN IN PRINT ORDER`**

---

## 4. ESC/P Printer Codes & The Real Key

So the key is the **"emphasis run in print order"**. What does that mean?

Remember the hint about raw printer output and the weird typos in the text?
If you've ever dealt with dot-matrix printers, `NOTICE09.PRN` is formatted in **Epson ESC/P** control codes:
- `ESC E` (`1B 45`): Select **emphasized** (bold) mode
- `ESC F` (`1B 46`): Cancel **emphasized** mode

When the file was opened as text, the escape byte `1B` was dropped or non-printable, leaving just the letters `E` and `F` sandwiching the bolded character! That's where all the typos came from:
- `LO` + `E` + `B` + `F` → `LOEGF` (letter `B`)
- `TRANSCRI` + `E` + `B` + `F` → `TRANSCRIEBFEEDF` (letter `B`, then `E` + `D` + `F`)
- `T` + `E` + `E` + `F` + `LETYPE` → `TEEFLETYPE` (letter `E`)
- `N` + `E` + `O` + `F` → `NEOF` (letter `O`)

Opening `NOTICE09.PRN` in `xxd` makes this crystal clear:

```text
00000000: 1b45 471b 4640 434f 4e54 494e 5549 5459  .EG.F@CONTINUITY
00000010: 2057 4154 4348 204c 4f1b 4542 1b46 202d   WATCH LO.EB.F -
...
00000060: 0d0a 5452 414e 5343 5249 1b45 421b 4654  ..TRANSCRI.EB.FT
00000070: 4545 1b45 441b 4620 4652 4f4d 2054 1b45  EE.ED.F FROM T.E
00000080: 451b 464c 4554 5950 4520 5441 5045 2c20  E.FLETYPE TAPE,
```

Every bolded letter is wrapped in `\x1bE <char> \x1bF`.

We just pull out every emphasized byte in print order:

1. `G` (at `0x0000`)
2. `B` (at `0x0019`)
3. `D` (at `0x0069`)
4. `E` (at `0x0078`)
5. `O` (at `0x008e`)
6. `A` (at `0x00af`)
7. `O` (at `0x00d2`)
8. `O` (at `0x00eb`)
9. `S` (at `0x00fe`)
10. `C` (at `0x0113`)
11. `M` (at `0x015e`)
12. `L` (at `0x0163`)

Putting them together gives our 12-byte key:
```text
GBDEOAOOSCML
```

---

## 5. Decrypting SEALED.BIN

Now that we have the key, we just XOR it against `SEALED.BIN`:

```python
from pathlib import Path

KEY = b"GBDEOAOOSCML"

ciphertext = Path("SEALED.BIN").read_bytes()

plaintext = bytes(
    byte ^ KEY[i % len(KEY)]
    for i, byte in enumerate(ciphertext)
)

print(plaintext.decode("ascii"), end="")
```

Running it:

```bash
$ python3 solve.py
CONTINUITY NOTICE 9 OF 9 FROM P-0
CLEARANCE flag{n0t1c3_n1n3_jr_70b90f256d}
CHK 4DA9EDC6
```

The checksum `CHK 4DA9EDC6` matches `SEAL CHK 4DA9EDC6` from `NOTICE09.PRN`, so we know the decryption is 100% correct.

**Flag:** `flag{n0t1c3_n1n3_jr_70b90f256d}`
