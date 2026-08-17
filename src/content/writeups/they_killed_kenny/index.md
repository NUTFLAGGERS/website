---
title: "oh my god, they killed kenny! (osint)"
pubDate: "2026-04-04"
updatedDate: "2026-04-04"
event: "sillyctf-2"
author: ""
score: ""
description: |
  > Mmmph mmph mmmph! (Translation: Oh my God! They killed, buried, and dug up Kenny… again.)
  > Kenny’s grave was on display in the real-life town that inspired South Park, at a local museum. A few days ago, the grave was dug up and Kenny is now missing. So is an out-of-service steam locomotive from the museum.
  > Figure out which railroad Kenny is on, based on the type of steam locomotive, so we can find him (or the bastard that took him). Submit the flag in lowercase.
  > For example, if the railroad was Blue Coastal Rail, then the flag would be sillyCTF{bcr}
tags: ["osint"]
---

Fairplay, Colorado inspired South Park (there's a real basin named South Park)

There's literally also a South Park City museum there [https://www.tripadvisor.com/Attractions-g33416-Activities-c49-Fairplay_Colorado.html](https://www.tripadvisor.com/Attractions-g33416-Activities-c49-Fairplay_Colorado.html)

The locomotive on display is a 1914 Porter (Company) Mogul (2-6-0 wheel arrangement) Locomotive [https://www.reddit.com/r/cyanotypes/comments/1fjltt3/1914_porter_mogul_locomotive_south_park_city/](https://www.reddit.com/r/cyanotypes/comments/1fjltt3/1914_porter_mogul_locomotive_south_park_city/)

[https://en.wikipedia.org/wiki/Denver,_South_Park_and_Pacific_Railroad](https://en.wikipedia.org/wiki/Denver,_South_Park_and_Pacific_Railroad)
And hence this should be the railroad

The problem is flags:

There's like 10 million possible permutations cos the line kept changing hands the post doesn't say whether to include commas

All combinations: sillyCTF{denver, south park and pacific railroad}sillyCTF{denver south park and pacific railroad}sillyCTF{denver, south park and pacific rail}sillyCTF{denver south park and pacific rail}sillyCTF{denver, south park and pacific railway}sillyCTF{denver south park and pacific railway}sillyCTF{denver, leadville and gunnison railroad}sillyCTF{denver leadville and gunnison railroad}sillyCTF{denver, leadville and gunnison railway}sillyCTF{denver leadville and gunnison railway}sillyCTF{denver, leadville and gunnison rail}sillyCTF{denver leadville and gunnison rail}

Other notable possible options:sillyCTF{union pacific rail}sillyCTF{union pacific railway}sillyCTF{colorado and southern rail}sillyCTF{colorado and southern railway}sillyCTF{denver and rio grande rail}sillyCTF{denver and rio grande railroad}

—

Ok new combossillyCTF{dsp&pr}sillyCTF{dspapr}sillyCTF{dl&gr}sillyCTF{dlagr}sillyCTF{upr}sillyCTF{csr}sillyCTF{d&rgr}sillyCTF{dargr}

**flag:** sillyCTF{dspprr}
