---
title: "ritsec-ctf — Pirate's Lost Log (Misc)"
pubDate: "2026-04-05"
updatedDate: "2026-04-05"
event: "ritsec-ctf"
author: ""
score: ""
description: |
  > Rumors have spread across the seven seas of a legendary pirate's log, hidden not on a physical island, but within the digital currents of the Domain Name System. This log, said to contain the coordinates of a vast buried treasure, was split into fragments and scattered across a secluded zone (linksnsec.stellasec.com) by a cunning old sea dog.
  > The fragments are concealed within the DNS, each leading to the next like a chain of clues on a treasure map. Our best guess is that the final piece of the puzzle, the one that reveals the treasure's location, will be the longest entry in the entire record, standing out from the rest.
  > Your mission: navigate the hidden paths within the pirate's domain. Follow the digital breadcrumbs to uncover every fragment. Find the single data record with the longest content to recover the complete log and claim the treasure.
  > The DNS server responds to TCP only, either query it over TCP or use a public recursive resolver (1.1.1.1, etc) to access it. This challenge is exclusively DNS and not web!
tags: ["misc"]
---

# Pirate's Lost Log — ritsec-ctf (Misc)

Script to run dig commands. walks through subdomains starting from CURRENT. first read the TXT record to get the log fragment and check its length. next, read the NSEC record to find out which subdomain to query next.

file: walker.py

the longest string is 142 chars n is the flag: thebartentersawcaptainjackwalkintothebarwiththeshipswheelaroundhisnutsthebartenderaskedhimwhatwasgoingoncaptainjackrepliedyaaritsdrivingmenuts
