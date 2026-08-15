---
title: "FindTheFeed — Social Media OSINT"
pubDate: "2025-03-10"
event: "picoCTF 2025"
author: "maejikal"
score: "200 pts"
tags: ["osint"]
description: "Tracing cross-platform social media handles and geolocating image metadata."
---

# FindTheFeed (OSINT - 200 pts)

## Investigation Path
Given a target handle `@cyber_nutflagger`, OSINT techniques were utilized to map out associated accounts:

1. **Username Enumeration**:
   Used WhatsMyName and Sherlock scripts to identify profiles on Mastodon and Bluesky.

2. **EXIF Metadata & Geolocation**:
   Downloaded an image from the target's public feed. Extracted GPS EXIF tags pointing to coordinates: `1.2966° N, 103.7764° E` (NUS School of Computing).

3. **Flag Retrieval**:
   Found the hidden flag inside the ALT text of a pinned post: `picoCTF{0s1nt_g30l0c4t10n_m4st3r_2025}`.
