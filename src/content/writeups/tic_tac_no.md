---
title: "lactf-26 — tictactoe (pwn)"
pubDate: "2026-02-13"
updatedDate: "2026-02-13"
event: "lactf-26"
author: "pucaru"
score: ""
description: |
  > Tic-tac-toe is a draw when played perfectly. Can you be more perfect than my perfect bot?
  > 
  > nc chall.lac.tf 30001
  > 
  > Flag Format: `lactf{}`
tags: ["pwn"]
---

# tictactoe — lactf-26 Writeup

- **Challenge:** tictactoe
- **Category:** pwn
- **Flag:** `lactf{th3_0nly_w1nn1ng_m0ve_1s_t0_p1ay}`

---

For indexes `< 0` & `>= 9`, it will run:

```c
board[index]  = player;
```

```bash
gdb ./chall # To get more info

(gdb) p &board
$1 = (<data variable, no debug info> *) 0x4068 <board>
(gdb) p &computer
$2 = (<data variable, no debug info> *) 0x4051 <computer>
(gdb)
```

`0x4068 - 0x4051 = 0x0017 = 23 bytes`

So the `computer` variable can be accessed via `board[-23]`.

Because the code runs:

```c
board[index] = player;
```

This overrides the `computer` variable with `'X'`. After this, the computer puts `'X'` on the board. Since the player is also `'X'`, `winner == player` is now true!

![alt text](image-2.png)

**Flag:** `lactf{th3_0nly_w1nn1ng_m0ve_1s_t0_p1ay}`
---

## Files

- [Dockerfile](#)
- [chall.c](#)
- [chall](#)
