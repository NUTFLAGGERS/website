---
title: "Unpackme — UPX + Anti-debug Bypass"
pubDate: "2025-03-10"
event: "picoCTF 2025"
author: "w4ve"
score: "400 pts"
tags: ["rev"]
description: "Unpacking a modified UPX executable and defeating ptrace anti-debugging techniques."
---

# Unpackme (Reverse Engineering - 400 pts)

## Challenge Description
The binary `unpackme` was packed using a customized version of UPX with corrupted magic headers (`UPX!`) and built-in `ptrace(PTRACE_TRACEME)` anti-debugging hooks.

## Reversing Workflow

1. **Fixing the UPX Header**:
   Opening the binary in a hex editor showed the 4-byte header replaced with `NOPE`. Overwriting it back to `UPX!` allowed `upx -d unpackme` to decompress section headers.

2. **Bypassing `ptrace` Check**:
   Patching the check in GDB:
   ```gdb
   catch syscall ptrace
   commands
     set $rax = 0
     continue
   end
   ```

3. **Extracting Key Schedule**:
   Deobfuscating the decryption loop yields the flag: `picoCTF{upx_h34d3r_p4tch_4nd_ptr4c3_byp4ss}`.
