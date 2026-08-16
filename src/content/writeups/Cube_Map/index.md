---
title: "CDDC2026 — Cube Map (misc)"
pubDate: "2026-08-15"
updatedDate: "2026-08-15"
event: "CDDC2026"
author: ""
score: "400"
description: |
  > A 3D map has been delivered for your mission.
  > Navigate through the map to complete your task and retrieve the flag.
  >
  > Flag Format: `CDDC2026{}`
tags: ["misc"]
---

# Cube Map — CDDC2026 Writeup

- **Challenge:** Cube Map
- **Category:** Misc
- **Points:** 400 (decayed to ~330)
- **Flag:** `CDDC2026{Thr33_cub3d_T1m35_Thr33_cub3_puzzl35!}`

---

## 1. The description and the hints in it

> A 3D map has been delivered for your mission.
> Navigate through the map to complete your task and retrieve the flag.
>
> Flag Format: CDDC2026{}

Three deliberate hints are buried in this short text:

| Phrase                                                                                                | What it actually tells you                                                                                                         |
| ----------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| **"3D map"** + title **"Cube Map"**                                                                   | The artifact is a **3‑dimensional** structure, not flat images. The grids you download are _slices_ of a cube.                     |
| **"Navigate _through_ the map"**                                                                      | The answer is the **interior / negative space** of the cube — the parts you can move _through_ (empty voxels), not the solid bulk. |
| **The flag itself** — `Thr33_cub3d_T1m35_Thr33_cub3_puzzl35` ("three cubed times three cube puzzles") | Confirms the structure post‑hoc: **9 puzzles × 9 layers = 9³**. Each file is a 9×9×9 cube; there are 9 of them.                    |

The download button linked a **Google Drive folder**, not a direct file — a small bit of friction (you can't just `wget` the attachment; you need `gdown` or the share UI).

---

## 2. Recon — what's in the box

```
chal.zip
└── chal/
    ├── map1.png … map9.png     # nine ~2000×2000 puzzle images
    └── flag.txt.zip            # 48-byte flag, ENCRYPTED
```

`flag.txt.zip` metadata:

- `flag.txt` — 48 bytes, `compress_type = 0` (stored), `flag_bits = 0x1` (encrypted).
- Extra field is `0x000a` (NTFS timestamp), **not** `0x9901` → so it's **traditional ZipCrypto**, not AES.

So the whole challenge reduces to: **recover the ZipCrypto password from the nine images.**

Each `mapN.png` is titled `CUBE MAP - Puzzle N` and contains **nine 9×9 grids** labelled `z = 1 … z = 9`. Each grid has numbers along the top (column clues) and left (row clues). They are **nonograms (Picross)**. Stacking the 9 solved `z`-layers gives one **9×9×9 voxel cube** per puzzle → 9 cubes.

### The clue encoding (the first real puzzle)

The clue numbers are **not printed as digits** — each is a tiny **3×3 dot‑matrix glyph**, and the **number of lit dots = the clue value**:

```
1 = single dot      4 = four corners     7 = ###/#.#/#.#
2 = two corners     5 = X (corners+ctr)  8 = ###/#.#/### (hollow)
3 = "/" diagonal    6 = #.#/#.#/#.#       9 = full 3×3 block
```

A fully filled column (clue 9) shows up as a solid 3×3 block of dots, which is the giveaway that _count = value_.

---

## 3. Solving — step by step

The hard part is mechanical: there are **81 nonograms** to read and solve, so it has to be automated. Pipeline:

### 3.1 Read the dots (`extract.py`)

- Threshold the bright cyan dots. **Gotcha:** the puzzle title `Z = N` and headers are _also_ cyan. They are a slightly different shade — dots are green‑cyan `(0,230,240)`, UI text is blue‑cyan `(0,212,255)`. Filtering on **`B − G < 22`** cleanly drops all titles.
- Split each clue _line_ into glyphs by 1‑D gaps (within‑digit dot gap ≤16 px, between‑digit ≥20 px → split at 18). Count dots per glyph = clue number.

### 3.2 Find the grids (`geom.py`)

Every map has a different image size and slightly irregular grid placement, so geometry can't be hard‑coded. Grid lines all intersect, so each grid is **one connected component** of the grid‑line mask → label them, take the 9 large square components, refine each grid's exact origin from its line projection. Cell size came out to a constant **54 px**.

### 3.3 Solve the nonograms (`nonogram.py`)

Standard line‑solver: enumerate candidate fills per row/column, **constraint‑propagate** the cells that are forced, then DFS on the rest. Every one of the **81 layers solved to a unique solution**.

> **Edge bug worth noting:** in tightly packed maps, a neighbouring grid's clues bleed into the target grid's clue margin (separated by a big gap). Fix: keep only the digit‑groups _contiguous from the grid edge_, stop at any gap > 45 px. That took the inconsistent‑layer count from 48 → 6 → **0**.

### 3.4 Assemble & read the cubes (`solve_all.py`)

- Stack the 9 layers into `cube[z][y][x]`. Each cube is a **nearly‑solid block (~660/729 voxels)** with a shape **carved out of it** — exactly the "navigate _through_" hint. The information is in the **empty** voxels.
- The empty voxels form a **3D "trip‑let"**: projecting the holes onto a face yields a **letter/digit**. Reading each cube's clearest face:

| map   | 1     | 2     | 3     | 4     | 5              | 6     | 7     | 8     | 9     |
| ----- | ----- | ----- | ----- | ----- | -------------- | ----- | ----- | ----- | ----- |
| glyph | **3** | **9** | **B** | **X** | **@** (spiral) | **M** | **C** | **P** | **U** |

→ password **`39BX@MCPU`**.

### 3.5 Open the flag

```python
import zipfile
zipfile.ZipFile('flag.txt.zip').read('flag.txt', pwd=b'39BX@MCPU')
# b'CDDC2026{Thr33_cub3d_T1m35_Thr33_cub3_puzzl35!}\n'
```

---

## 4. The "exploit" / TL;DR

1. `gdown` the Drive folder → 9 nonogram PNGs + an encrypted ZipCrypto archive.
2. OCR the 3×3 dot glyphs (dot‑count = clue value); colour‑filter to drop title text.
3. Auto‑detect grid geometry (connected grid‑line components).
4. Solve all 81 9×9 nonograms (propagation + DFS).
5. Stack into 9 cubes; the **empty voxels** of each cube spell one character: `39BX@MCPU`.
6. That string is the **ZipCrypto password** → unzip `flag.txt`.

`CDDC2026{Thr33_cub3d_T1m35_Thr33_cub3_puzzl35!}`

### Alternative (cheese) path

The archive is **traditional ZipCrypto**, which is cryptographically broken. Because the plaintext begins with the known flag prefix `CDDC2026{`, a **known‑plaintext attack** (`bkcrack`) can recover the internal keystream and decrypt `flag.txt` **without ever solving the cubes**. It's messier than the intended solve here, but worth remembering: _stored + ZipCrypto + known prefix = decryptable without the password._

---

## 5. Files

```
challenges/737/distfiles/extracted/chal/
  extract.py     # dot/glyph OCR
  geom.py        # per-map grid detection
  nonogram.py    # 9x9 nonogram solver
  solve_all.py   # full pipeline -> cube*.npy
  best_faces.png # the 9 rendered glyphs
  FLAG.txt
```
