---
title: "lactf-26 — lactf-invoice-generator (web)"
pubDate: "2026-02-07"
updatedDate: "2026-02-07"
event: "lactf-26"
author: "ベイ先生"
score: ""
description: ""
tags: ["web"]
---

# lactf-invoice-generator — lactf-26 (web)

dist.tar.gz

- invoice generator takes in input (processed by puppeteer). did a quick google search on puppeteer vuln and SSRF came up
  - mentions about using iframe tags injected into the input and from here you can load any other remote services.
- based on docker compose structure, flag and the invoice generator services are on different containers, BUT you can access them based on their container name among the docker containers.
- flag.js file states that loading of file involves a GET request to port 8081 of the flag server and with the URI of /flag

```javascript
const http = require("http");

const FLAG = process.env.FLAG || "lactf{fake_flag}";
const PORT = 8081;

const server = http.createServer((req, res) => {
  if (req.method === "GET" && req.url === "/flag") {
    res.writeHead(200, { "Content-Type": "text/html" });
    res.end(`<div><strong>FLAG:</strong> ${FLAG}</div>`);
    return;
  }
```

- just needed to inject the iframe in the "description" field.
  ![Reference](./image.png)
  ![Reference](./image_1.png)
