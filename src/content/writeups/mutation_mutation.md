---
title: "lactf-26 — mutation-mutation (web)"
pubDate: "2026-02-09"
updatedDate: "2026-02-09"
event: "lactf-26"
author: "LevelOP"
score: ""
description: |
  > It's a free flag! You just gotta inspect the page to get it. Just be quick though... the flag is constantly mutating. Can you catch it before it changes?
  > 
  > mutation-mutation.chall.lac.tf
  > 
  > Flag Format: `lactf{}`
tags: ["web", "javascript", "dom"]
---

# mutation-mutation — lactf-26 Writeup

- **Challenge:** mutation-mutation
- **Category:** Web
- **Flag:** `lactf{с0nѕtаnt_mutаtі0n_1sfun!}` _(Note: May contain homoglyphs/Cyrillic characters based on the mutation state)_

---

## Challenge Description

> It's a free flag! You just gotta inspect the page to get it. Just be quick though... the flag is constantly mutating. Can you catch it before it changes?
>
> mutation-mutation.chall.lac.tf

The description heavily implies that the flag is present in the DOM but is actively being altered by JavaScript (likely via `setInterval`, `requestAnimationFrame`, or a `MutationObserver`).

---

- **Artifacts:** `image.png`, `message.txt`
- **Flag:** `lactf{с0nѕtаnt_mutаtі0n_1sfun!ІlІ1| ض픋ԡೇ∑ᦞ୞땾᥉༂↗ۑீ᤼യ⌃±❣Ӣ◼ௌௌௌௌௌ}`

---

## Remaining Question

**The Question:** _Aside from using `console.log` to manually cycle through the options, is there a way to de-obfuscate this to something useful?_

---

## Files

- [image.png](#)
- [message.txt](#)
