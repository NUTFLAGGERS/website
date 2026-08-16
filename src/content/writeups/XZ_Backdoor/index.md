---
title: "CDDC2026 — XZ Backdoor (reversing/forensics)"
pubDate: "2026-08-15"
updatedDate: "2026-08-15"
event: "CDDC2026"
author: ""
score: "370-390"
description: |
  > During a supply chain security audit of an open-source compression library, our team
  > discovered suspicious modifications to the build system. The changes closely resemble
  > the techniques used in the XZ Utils compromise (CVE-2024-3094)... Trace the attack chain,
  > extract the hidden payload, and recover the secret.
  > 
  > Flag Format: `CDDC2026{}`
tags: ["reversing", "forensics"]
---

# XZ Backdoor — CDDC2026 (Reversing / Forensics, 370–390 pts)

**Flag:** `CDDC2026{1func_r3s0lv3r_h1j4ck_jia_tan_w4s_h3r3}`

---

## 1. Challenge summary

> During a supply chain security audit of an open-source compression library, our team
> discovered suspicious modifications to the build system. The changes closely resemble
> the techniques used in the XZ Utils compromise (CVE-2024-3094)... Trace the attack chain,
> extract the hidden payload, and recover the secret.

Files provided (in `chal.zip`):

```
challenge/build-to-host.m4          <- modified autotools macro (entry point)
challenge/tests/files/*.xz          <- 5 "test fixture" compression samples
challenge/README.txt
```

This is a faithful re-creation of the real **xz-utils backdoor (CVE-2024-3094 / "Jia Tan")**:
a malicious `m4` macro in the release tarball reconstructs a payload at `./configure` time
from files that masquerade as corrupted compression test cases.

---

## 2. Hints from the description and how each was used

| #   | Hint (from README)                                                                                       | How it was used                                                                                                                                                                                                                       |
| --- | -------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | _"payload hidden inside test fixture files that appeared to be corrupted compression samples"_           | Told us the `tests/files/*.xz` are not real test data — one of them carries the payload. Focused attention on `bad-3-corrupt_lzma2.xz`.                                                                                               |
| 2   | _"Look at how grep is used"_ to identify the payload file                                                | The macro runs `grep -aErls "#{4}[[:alnum:]]{5}####"` — i.e. it locates the file containing a tag of the form `####XXXXX####`. Running that grep ourselves pinpointed the carrier file + tag `####bkd0r####`.                         |
| 3   | _"extraction pipeline involves multiple stages... pay attention to xz and tr commands"_                  | The macro does `tail -n +2 \| xz -dc` to peel off the tag line and decompress stage 1. Stage 1 then base64-decodes an ELF object. (No `tr` byte-substitution stage was needed here — a small simplification vs. the real CVE.)        |
| 4   | _"payload targets a specific well-known network service... what it hooks and what key material it uses"_ | The ELF hooks **`RSA_private_decrypt`** (the OpenSSL/OpenSSH path, exactly like the real sshd backdoor). The "key material" is an RSA-encrypted AES key + RSA modulus baked into the object. Recovering the flag = breaking that RSA. |

---

## 3. Attack chain

```
build-to-host.m4
   │  grep -aErls "####[alnum]{5}####"  tests/files/
   ▼
bad-3-corrupt_lzma2.xz   (tag line: "####bkd0r####")
   │  tail -n +2 | xz -dc            (drop tag line, decompress)
   ▼
stage1.sh                (POSIX sh "build configuration helper")
   │  base64 -d $payload  > $obj
   ▼
backdoor.o               (ELF x86-64 relocatable object, GCC 13.4.0)
   • hooks RSA_private_decrypt
   • _bd_enc_flag      (80 B)  = IV(16) ‖ AES-256-CBC ciphertext(64)
   • _bd_enc_aes_key   (256 B) = RSA-encrypted AES key
   • _bd_rsa_n         (256 B) = RSA-2048 modulus  ← weak!
```

### 3.1 Stage 0 — the malicious macro

`build-to-host.m4` (`LC_BUILD_TO_HOST`) hides the trigger inside innocuous-looking
autotools cross-compilation logic:

```sh
gl_am_configmake=`grep -aErls "#{4}[[:alnum:]]{5}#{4}" $srcdir/tests/files/ 2>/dev/null`
...
tail -n +2 "$gl_localedir_data" 2>/dev/null | xz -dc 2>/dev/null > "$gl_localedir_tmp"
chmod +x "$gl_localedir_tmp"
. "$gl_localedir_tmp" "$gl_cv_host_obj"      # source stage-1, passing an output path
```

Reproduced manually:

```bash
grep -aErls "#{4}[[:alnum:]]{5}#{4}" tests/files/
#  -> tests/files/bad-3-corrupt_lzma2.xz
grep -aEro "#{4}[[:alnum:]]{5}#{4}" tests/files/bad-3-corrupt_lzma2.xz
#  -> ####bkd0r####
tail -n +2 tests/files/bad-3-corrupt_lzma2.xz | xz -dc > stage1.sh
```

### 3.2 Stage 1 — shell dropper

`stage1.sh` exports the path argument, then base64-decodes a blob into that path:

```sh
export gl_path_map="$1"
payload='f0VMRgIBAQM...'          # base64 of an ELF .o
printf '%s' "$payload" | base64 -d > "$gl_path_map"
```

Decoding the blob yields **`backdoor.o`** (6992 bytes, `ELF 64-bit relocatable`).

### 3.3 Stage 2 — the backdoor object

Symbol table (`_bd_*`) and string table make the intent obvious:

```
_bd_hooked_rpd     hooked RSA_private_decrypt
_bd_orig_rpd       saved original
_bd_do_decrypt     flag-decryption routine
_bd_enc_flag       .rodata+0    (80 B)
_bd_enc_aes_key    .rodata+96   (256 B)
_bd_rsa_n          .rodata+352  (256 B)
strings: RSA_private_decrypt, RSA_get0_key, BN_bn2bin, EVP_aes_256_cbc,
         EVP_DecryptInit_ex/Update/Final_ex, /proc/self/cmdline, /proc/self/comm
```

It resolves OpenSSL functions via `dlsym` at runtime (GOT/IFUNC-style resolver hijack,
mirroring the real backdoor's `_bd_crc64_resolve`).

---

## 4. Reversing the crypto (the key step)

Disassembling `_bd_do_decrypt` and resolving the relocations gives the exact data flow:

```
RSA_private_decrypt(flen=256, from=_bd_enc_aes_key, to=buf, rsa=<conn key>, padding=3)
                                                                          ^ 3 = RSA_NO_PADDING
key  = buf[224:256]          # last 32 bytes of the raw 256-byte RSA block
iv   = _bd_enc_flag[0:16]    # first 16 bytes of the flag blob ARE the IV
ct   = _bd_enc_flag[16:80]   # remaining 64 bytes = AES-256-CBC ciphertext
EVP_DecryptInit_ex(ctx, EVP_aes_256_cbc(), NULL, key, iv)
EVP_DecryptUpdate(...) ; EVP_DecryptFinal_ex(...)
```

Reloc resolution that nailed the offsets:

```
@364  from  -> .rodata+96   (_bd_enc_aes_key)
@438  iv    -> .rodata+0    (_bd_enc_flag[0:16])
@459  ct    -> .rodata+16   (_bd_enc_flag[16:])
```

So the AES key is whatever the **server's RSA private key** produces from
`_bd_enc_aes_key`. Normally that key only exists on the victim sshd host — but the
challenge ships the modulus `_bd_rsa_n`, and it is **deliberately weak**.

### 4.1 Breaking the RSA

`_bd_rsa_n` is a 2048-bit modulus whose two primes are almost equal (they differ by ~280),
so **Fermat factorization** succeeds in a handful of iterations — no need for yafu/SIQS:

```python
a = isqrt(n); a += (a*a < n)
while not is_square(a*a - n): a += 1
b = isqrt(a*a - n); p, q = a-b, a+b        # found almost immediately
```

(yafu would also crack it instantly since it tries Fermat first, but plain Fermat is enough.)

With `p,q`: `d = e^{-1} mod (p-1)(q-1)`, `e = 65537`.

---

## 5. Exploit / solver

```python
import math
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

n   = int("caaba4a3...c9", 16)      # _bd_rsa_n      (256 B)
eak = int("34302655...c8", 16)      # _bd_enc_aes_key(256 B)
ef  = bytes.fromhex("11d5f24a...d70c")  # _bd_enc_flag (80 B)

# Fermat factor (primes are ~280 apart)
a = math.isqrt(n);  a += (a*a < n)
while True:
    b2 = a*a - n; b = math.isqrt(b2)
    if b*b == b2: break
    a += 1
p, q = a-b, a+b
d = pow(65537, -1, (p-1)*(q-1))

# RSA NO_PADDING decrypt -> 256-byte raw block; AES key = last 32 bytes
raw = pow(eak, d, n).to_bytes(256, "big")
key = raw[224:256]

# AES-256-CBC: IV is the first 16 bytes of the flag blob
iv, ct = ef[:16], ef[16:]
pt = Cipher(algorithms.AES(key), modes.CBC(iv)).decryptor()
flag = (pt.update(ct) + pt.finalize())
print(flag)   # CDDC2026{1func_r3s0lv3r_h1j4ck_jia_tan_w4s_h3r3}  + PKCS7 \x10*16
```

Output:

```
AES key : 6b11e6e4f69969ed54e2dbf0da8df7ce90d32c9f7f862cc60b6d0aa984cbb27a
plaintext: CDDC2026{1func_r3s0lv3r_h1j4ck_jia_tan_w4s_h3r3}\x10\x10...\x10
```

Clean PKCS#7 padding (`\x10` × 16) confirms the key and flag are correct.

---

## 6. Flag

```
CDDC2026{1func_r3s0lv3r_h1j4ck_jia_tan_w4s_h3r3}
```

The flag text itself nods to the technique (`1func_r3s0lv3r_h1j4ck` = the IFUNC resolver
hijack) and the original threat actor (`jia_tan`).

---

## 7. Takeaways / why it's "expert"

- **Multi-stage de-obfuscation**: m4 macro → tag-grep → `tail|xz` → base64 → ELF.
- **Static-only RE**: no readelf/objdump on the box — sections, symbols and relocations
  were parsed with `pyelftools` and code disassembled with `capstone`, then relocations
  resolved by hand to recover the precise `key/iv/ct` slicing.
- **The trick**: it _looks_ like you need the victim's RSA private key (as in the real
  CVE, where only the attacker could trigger it). The solvable twist is that the embedded
  modulus has near-equal primes → Fermat factorization → full private key → AES key → flag.

```

```
