---
title: "journaling (for)"
pubDate: "2026-03-28"
updatedDate: "2026-03-28"
event: "texsaw-2026"
author: "kuri"
score: ""
description: |
  > I was using this Windows machine for journaling and notetaking, but I think malware got onto it. Can you take a look and put together any evidence left on disk?
  > Note 1: Sufficient information is provided to figure out the order of flag segments Note 2: Flag segments should be connected by underscores and wrapped in texsaw{} Example flag format: texsaw{part1_part2_part3}

tags: ["for"]
---

# journaling — texsaw-2026 (for)

Found these two segments
flagsegment_3fd19982505363d0
flagsegment_u5njOurn@l
and this piece of info: Super important stolen data: username: user password: password

flagsegment_3fd19982505363d0
flagsegment_u5njOurn@l
flagsegment_4lter3d
flagsegment_unc0v3rs.txt
flagsegment_f1les.txt

**flag:**texsaw{u5njOurn@l_unc0v3rs_4lter3d_f1les_3fd19982505363d0}

there are a lot of folder and file deleted, i just carve out 1 by 1 and grep for flagsegment
