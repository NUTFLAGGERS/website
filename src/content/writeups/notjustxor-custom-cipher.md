---
title: "NotJustXOR — Custom Cipher Break"
pubDate: "2025-07-14"
event: "SekaiCTF 2025"
author: "w4ve"
score: "350 pts"
tags: ["crypto"]
description: "Cryptanalysis of a multi-stage XOR cipher with keystream reuse."
---

# NotJustXOR (Crypto - 350 pts)

## Challenge Description
The challenge implemented a stream cipher based on a linear congruential generator (LCG) combined with byte-wise XORing of repeated nonces.

## Cryptanalysis

Because nonces were reused across multiple messages, we applied Many-Time Pad (MTP) cryptanalysis:

1. **Keystream Recovery via Space Stripping**:
   Guessing spaces (`0x20`) across ciphertext pairs reveals candidate key bytes.

2. **LCG State Reconstruction**:
   Solving the linear system modulo $2^{64}$ using SageMath:

```python
from sage.all import *

# Recover LCG parameters (a, c, m)
# state_{n+1} = (a * state_n + c) mod m
```

Flag: `SEKAI{m4ny_t1m3_p4d_lcg_k3ystr34m_br34k}`.
