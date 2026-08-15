---
title: " CDDC2026 — Activation Image Challenge (misc)"
pubDate: "2026-08-15"
updatedDate: "2026-08-15"
event: "CDDC2026"
author: ""
score: ""
description: |
  > The image is only a trigger. The model output is the clue.
  > Find the hidden activation function for every round.
  >
  > `nc cddc2026.xyz 1339`
  > Flag Format: CDDC2026{}`
tags: ["misc", "ml"]
---

# CDDC2026 — Activation Image Challenge (misc)

**Flag:** `CDDC2026{perfect_activation_run}`

**Service:** `nc cddc2026.xyz 1339`
**Category:** misc / ML
**Format:** `CDDC2026{}`

---

## 1. Challenge description & the hints in it

> The image is only a trigger. The model output is the clue.
> Find the hidden activation function for every round.
>
> `nc cddc2026.xyz 1339`
> Flag Format: CDDC2026{}

Three lines, three hints — and reading them literally is the whole solve:

| Hint in the description                                  | What it actually means                                                                                                                                                                                    |
| -------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| _"The image is only a trigger."_                         | The image (an ASCII / PNG drawing of a hex digit `0-9a-f`) is **a red herring**. You do **not** need to classify it, OCR it, or care what symbol it shows. It just causes the model to produce an output. |
| _"The model output is the clue."_                        | The discriminating signal is in the **CNN's numerical output** — the `logits` and especially the `feature_summary` statistics returned by `QUERY`. That is where the answer is hidden.                    |
| _"Find the hidden activation function for every round."_ | Each round the CNN uses a **secret activation function** (one of 5). You must identify it from the output. _"every round"_ implies a multi-round chain where you must be right repeatedly.                |

So the task is **not** image recognition. It is: _given the numeric fingerprint a network leaves in its feature map, recover which activation function produced it._

---

## 2. Recon — learning the protocol

Connecting shows a line-based JSON protocol:

```
=== Activation Image Challenge (TCP) ===
Commands: HELP | INFO | QUERY | ANSWER <activation> | QUIT
```

`HELP` documents the four commands:

- `INFO` — current round metadata + image (ASCII + base64 PNG), **no model output**
- `QUERY` — runs the CNN on the current image and returns the **output summary** (3 per round)
- `ANSWER <activation>` — submit your guess
- `QUIT`

The `welcome` / `INFO` payload:

```json
{"type":"round_info","round_id":1,"symbol":"b","queries_used":0,"queries_left":3,
 "activation_candidates":["relu","leaky_relu","sigmoid","tanh","softplus"],
 "image_ascii":[...], "image_png_base64":"..."}
```

So the answer space is exactly **5 candidates**: `relu, leaky_relu, sigmoid, tanh, softplus`.

Crucially, `INFO` does **not** include the model output — only `QUERY` does. That confirms hint #2: you _must_ `QUERY` to get the clue.

### What `QUERY` reveals

```json
{"type":"query_result","round_id":1,
 "top3":[{"class":"9","prob":0.071,"logit":0.050}, ...],
 "logits":[0.0265, 0.0458, -0.0311, ...],            // 15 class logits
 "feature_summary":{"mean":0.00742,"std":0.054938,
                    "min":-0.113258,"max":0.145324,"positive_ratio":0.539062}}
```

The `top3`/`logits` are near-uniform noise (a random-weight CNN) — useless for reading the _symbol_, consistent with "the image is only a trigger." The gold is `feature_summary`: summary statistics of the **post-activation feature map**. An activation function is, by definition, a transform of a distribution — so its identity is written all over these stats.

### Game mechanics (discovered by probing)

I answered deliberately and watched the state machine:

- A **correct** `ANSWER` advances to the next round (`next_round` in the response).
- A **wrong** `ANSWER` → immediate `{"game_over":true}`. **One mistake ends the run.**
- The game runs **50 rounds**. Finishing all 50 yields `final_summary` with `"perfect": true` and the **flag**.

So this is a 50-in-a-row gauntlet: I need a classifier that is essentially 100% accurate, because a single error at round N throws away rounds 1..N-1.

---

## 3. The key insight — activation fingerprints

I collected ~20 `feature_summary` samples from fresh connections (QUERY → QUIT) and the 5 activations fall into **cleanly separated clusters**. The reason: each activation reshapes the pre-activation distribution in a mathematically distinct way.

Observed signatures of the post-activation feature map:

| Activation     | `positive_ratio` | `min`                   | `mean`     | Why                                                           |
| -------------- | ---------------- | ----------------------- | ---------- | ------------------------------------------------------------- |
| **sigmoid**    | **1.0**          | ~+0.257                 | ~**0.494** | maps ℝ→(0,1); values bunch around 0.5                         |
| **softplus**   | **1.0**          | ~+0.174                 | ~**0.707** | `log(1+e^x)` > 0 always; mean ≈ log2≈0.69, `max` can exceed 1 |
| **relu**       | ~0.5             | **exactly 0.0**         | ~0.018     | negatives clamped to a hard 0                                 |
| **leaky_relu** | ~0.5             | **small** neg (~−0.013) | ~0.017     | negatives scaled by α≈0.01 → tiny, but never exactly 0        |
| **tanh**       | ~0.5             | **strong** neg (~−0.11) | ~0.005     | symmetric (−1,1); \|min\| ≈ max, mean ≈ 0                     |

Two discriminators do all the work:

1. **`positive_ratio`** splits the always-positive activations (`sigmoid`, `softplus` → ratio = 1.0) from the rest (`relu`, `leaky_relu`, `tanh` → ratio ≈ 0.5).
2. **`min`** then separates the bottom three: exactly `0` → relu; tiny negative → leaky_relu; large negative → tanh. And **`mean`** separates sigmoid (~0.49) from softplus (~0.71).

This yields a trivial, fully **deterministic** decision tree — no ML, no LLM, no image processing required.

```python
def classify(fs):
    pr, mn, mean = fs['positive_ratio'], fs['min'], fs['mean']
    if pr > 0.95:                       # all outputs positive
        return 'sigmoid' if mean < 0.6 else 'softplus'
    if mn >= -1e-6:                     # clamped exactly at 0
        return 'relu'
    if mn > -0.05:                      # negatives compressed (alpha*x)
        return 'leaky_relu'
    return 'tanh'                       # symmetric, strong negatives
```

---

## 4. The exploit

Single persistent TCP connection. Per round: `QUERY` once → classify `feature_summary` → `ANSWER`. Repeat for all 50 rounds; the flag is in the final summary.

Full solver: [`solve_activation.py`](../../solve_activation.py). Core loop:

```python
class Conn:
    def __init__(self):
        self.s = socket.socket(); self.s.settimeout(10)
        self.s.connect(('cddc2026.xyz', 1339)); self.s.setblocking(False)
        time.sleep(1.0); self._drain()           # eat welcome banner
    def _drain(self, need_json=True, maxwait=6.0):
        buf = b''; t = time.time()
        while time.time() - t < maxwait:
            try:
                d = self.s.recv(65536)
                if d:
                    buf += d; t = time.time()
                    if need_json and b'\n' in buf and b'{' in buf:
                        time.sleep(0.05)
                        try:
                            while True:
                                d2 = self.s.recv(65536)
                                if not d2: break
                                buf += d2
                        except Exception: pass
                        break
            except BlockingIOError: time.sleep(0.02)
            except Exception: break
        return buf
    def cmd(self, c):
        self.s.sendall((c + '\n').encode()); return self._drain()

def main():
    c = Conn()
    while True:
        qr = next(j for j in jlines(c.cmd('QUERY')) if j.get('type') == 'query_result')
        act = classify(qr['feature_summary'])
        resp = c.cmd(f'ANSWER {act}')
        if b'CDDC2026{' in resp:
            print(resp.decode()); return        # flag is inside final_summary
        if b'game_over' in resp:                 # only reached on a wrong guess
            print('LOST:', resp.decode()); return
```

### Result

All 50 rounds classified correctly on the first full run:

```json
{"type":"final_summary","completed":true,"total_rounds":50,
 "answered_rounds":50,"correct_count":50,"accuracy":1.0,"perfect":true,
 "history":[ ... 50× {"correct":true} ... ],
 "flag":"CDDC2026{perfect_activation_run}"}
```

**Flag:** `CDDC2026{perfect_activation_run}`

---

## 5. Gotchas / notes

- **Don't touch the image.** Every minute spent OCR-ing the ASCII/PNG digit is wasted — the symbol is decorative. The description says so up front ("only a trigger").
- **`QUERY` before `ANSWER`.** `INFO`/`welcome` deliberately omit the model output. You need exactly **one** `QUERY` per round (the 3-query budget is a generous red herring; the result is deterministic per image).
- **One wrong answer = game over**, and there are 50 rounds, so the classifier must be ~100% reliable. The clean cluster separation makes the thresholds (`0.95`, `-1e-6`, `-0.05`, `mean 0.6`) very forgiving.
- **Rate limiting.** Opening many short-lived connections while sampling got my IP temporarily blocked (empty banner / `WinError 10053` connection-aborted). The fix is simply to back off briefly — and note the _real_ solve uses a **single** connection for all 50 rounds, so it never trips the limiter.
- **No "AI solving" needed.** Despite the ML framing, the solution is pure summary-statistics on the feature map: a 4-comparison decision tree.
