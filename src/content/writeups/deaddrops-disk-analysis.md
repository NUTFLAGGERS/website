---
title: "DeadDrops — Disk Image Analysis"
pubDate: "2025-04-21"
event: "Grey Cat The Flag 2025"
author: "w4ve"
score: "450 pts"
tags: ["forensics"]
description: "Forensic analysis of a corrupted raw disk image to recover deleted payloads."
---

# DeadDrops (Forensics - 450 pts)

## Challenge Summary
We were given a raw ext4 disk image (`deaddrops.img`) captured from a compromised Linux machine. The objective was to reconstruct deleted files and trace hidden exfiltration paths.

## Forensic Methodology

1. **Inspect File System Structure**:
   ```bash
   fls -r -p deaddrops.img
   ```

2. **Carving Deleted Inodes**:
   Extracting unallocated clusters revealed a steganographic payload embedded within unallocated sectors:
   ```bash
   scalpel deaddrops.img -c scalpel.conf
   ```

3. **Reconstructing the Flag**:
   Parsing the recovered memory artifact yields the flag: `grey{d1sk_3xp10r3r_f0r3ns1cs_m4st3r}`.
