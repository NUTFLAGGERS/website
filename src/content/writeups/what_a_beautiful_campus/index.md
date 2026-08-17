---
title: "Buildings around campus"
pubDate: "2026-04-04"
updatedDate: "2026-04-04"
event: "sillyctf-2"
author: "kuri™"
score: ""
description: |
  > I don't know where any buildings are around campus! It's even a headache looking on Google Maps.
  >
  > View Hint:It's case sensitive!
tags: ["osint"]
---

## 1. Challenge summary

> I don't know where any buildings are around campus! It's even a headache looking on Google Maps.
>
> View Hint:It's case sensitive!

---

## 2. Solution

```text
lon       lat           W    L
40.800306 -77.864929    1    7
40.805706 -77.863373    1    2
40.795194 -77.865206    1    6
40.801166 -77.857651    2    4
40.801121, -77.866701    2    6
40.798277 -77.867723    1    1
40.806253 -77.863788    1    1
40.795480 -77.868714    2    1
40.808229 -77.861386    3    4
40.791285 -77.869983    1    5
40.812099 -77.856111    6    3
40.793844 -77.867627    1    4
40.801827 -77.862961    1    3
40.800542 -77.86032    1    5
40.797989 -77.870718    1    4
40.789306 -77.873184    2    2
40.80075 -77.856543    1    4
40.801619 -77.85779    1    2
40.800986 -77.853924    1    5
40.801851 -77.866561    1    3
40.807525 -77.859268    1    7
40.798052 -77.865932    4    2
40.805499 -77.860871    2    3
40.796922 -77.865774    2    5
40.798578 -77.856932    1    2
40.796547 -77.85985    1    1
40.806658 -77.856919    1    3
40.803458 -77.863758    4    5

sillyCTB?h?ts?l?to?bueldiNgs

Penn State University Park

use each coordinate as a point query against PSU’s University Park Buildings layer

```
