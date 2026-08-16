---
title: "texsaw-2026 — Lost My Keys (for)"
pubDate: "2026-03-28"
updatedDate: "2026-03-28"
event: "texsaw-2026"
author: "slacksleepsloth"
score: ""
description: |
  > I can't find my original house key anywhere! Can you help me find it? 
  > Here's a picture of my keys the nanny took before they were lost. It must be hidden somewhere!
  > Flag format: texsaw{you_found_me_at_key}
tags: ["for"]
---

# Lost My Keys — texsaw-2026 (for)

—
First clue is that the file size is rlly big, Running strings [image.png]
Running binwalk to extract files:[image.png]
You get 2 more pictures:Temoc_keyring(orig).png, where_are_my_keys.png

rgb values on the top left seems to have difference of 1[image.png]

pixels 0 to 215 is 216 pixels and 216 / 8 is 27
take the ones which are different as 1 and the ones which are not different as 0
get the binary and throw it into bin to string u get the flag [image.png]
