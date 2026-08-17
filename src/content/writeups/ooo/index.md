---
title: "lactf-26 — ooo (rev)"
pubDate: "2026-02-09"
updatedDate: "2026-02-09"
event: "lactf-26"
author: "Level"
score: ""
description: |
  Surely everyone knows the difference between the Cyrillic small letter o, the Greek small letter omicron, and the Latin small letter o, right?
tags: ["rev"]
---

ooo.py

Inspecting the code, its those cancer things where u have to know what character as they look similar but have different unicode

Reference: [https://gist.github.com/StevenACoffman/a5f6f682d94e38ed804182dc2693ed4b](https://gist.github.com/StevenACoffman/a5f6f682d94e38ed804182dc2693ed4b)
![- Screenshot](./image.png)

Simplifies to:
index = ö XOR ((ord(c1)ord(c2)) % ord(c1)) = ö XOR 0 = ö (since (ab) % a = 0 for a != 0
ό = ord(guess[ö]) ὃ = ord(guess[ö+1])

Means
ord(ci​)+ord(ci+1​)=ὁ[i]

And thus
ord(ci+1​)=ὁ[i]−ord(ci​)

Start of the flag is lactf{ so

for i=0,
ord(c0) is 108 for "l" and ord(c1) is 97 for "a"

Repeat and lookup (can probably python this)

lactf{gоοօỏơóὀόὸὁὃὄὂȯöd_j0b}


## Step 1

We observe that each of the unicode characters stands for a different arithmetic operation

| Original (Unicode)  | Readable name | Operation |
| ------------------- | ------------- | --------- |
| `о` (Cyrillic)      | `add`         | `a + b`   |
| `ο` (Greek omicron) | `sub`         | `a - b`   |
| `օ` (Armenian)      | `mul`         | `a * b`   |
| `ỏ`                 | `floordiv`    | `a // b`  |
| `ơ`                 | `xor`         | `a ^ b`   |
| `ó`                 | `or_`         | `a \| b`  |
| `ὀ` (Greek)         | `and_`        | `a & b`   |
| `ὸ` (Greek)         | `sub_rev`     | `b - a`   |
| `ὄ` (Greek)         | `first`       | `a`       |
| `ὂ` (Greek)         | `second`      | `b`       |
| `ȯ`                 | `mod`         | `a % b`   |

## Step 2

Since it's Python, we look at the next couple lines to see what they do

```Python
if (len(guess) < len(ὁ)):
    print("That's too short :(")
    exit()

```

We can see that this is just a check for how long the guessed string is (which is 27 characters)

```Python
for ö in range(len(ὁ)-1):
for i in range(len(targets) - 1): // In human readable format

```

I did not know any unicode character could be a loop counter but the more you know ig

```Python
    ό = ord(guess[ö])
    ὃ = ord(guess[ö+1])

    // Human readable format
    curr = ord(guess[i])
    nxt = ord(guess[i + 1])

```

This returns the unicode character number of two consecutive numbers in `guess`

## Step 3

```Python
    if (о(ὄ(ό,ὃ),ὂ(ό,ὃ)) != ὁ[ơ(ö,ȯ(օ(ό,ὃ),ό))]):

```

This is the complicated portion. We need to simplify this expression to figure out what it means. Let's look at each side:

### LHS

`о(ὄ(ό,ὃ), ὂ(ό,ὃ))`

- о (Cyrillic “o”) is the function that returns a + b
- ὄ (Greek omega with psili and oxia) returns a → so ὄ(ό,ὃ) = ό
- ὂ (Greek omega with psili and varia) returns b → so ὂ(ό,ὃ) = ὃ

Hence:

```Python
о(ὄ(ό,ὃ), ὂ(ό,ὃ)) = о(ό, ὃ)
                  = ό + ὃ
                  = ord(guess[ö]) + ord(guess[ö+1])

```

Which is the sum of 2 consecutive character codes

### RHS

`ὁ[ơ(ö, ȯ(օ(ό,ὃ), ό))]`

We solve the inner section first:

`ȯ(օ(ό,ὃ), ό)`

- օ (Armenian “o”) is a * b → օ(ό,ὃ) = ό * ὃ
- ȯ (Latin o with dot above) is a % b (modulo)

Hence:

```Python
օ(ό,ὃ) = ό * ὃ
ȯ(օ(ό,ὃ), ό) = ȯ(ό*ὃ, ό)
             = (ό * ὃ) % ό

```

We observe that (a * b) % a is 0 (unless a =/= 0), so `ȯ(օ(ό,ὃ), ό) = 0`

Solving the outermost function:

```Python
ơ(ö, ȯ(օ(ό,ὃ), ό)) = ơ(ö, 0)
                   = ö

```

Translating the entire snippet into something human readable:

```Python
if add(first(curr, nxt), second(curr, nxt)) != targets[xor(i, mod(mul(curr, nxt), curr))]:

if (curr + nxt) != targets[i]: // Simplified further

```

## Step 4

We already know that the first 5 letters of the flag are `lactf{`, so we can build a simple solver to iterate through the list and recover the flag

It will set `next_code = ὁ[i] - ord(flag[i])`, then append `chr(next_code)` to the flag (or set `flag[i+1] = chr(next_code)`)

The resulting flag is `lactf{gоοօỏơóὀόὸὁὃὄὂȯöd_j0b`
