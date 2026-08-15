---
title: "Linux Kernel Use-After-Free Exploitation Deep Dive"
pubDate: "2025-05-18"
updatedDate: "2025-05-20"
type: "individual"
author: "w4ve"
tags: ["pwn", "rev"]
---

# Linux Kernel Use-After-Free Exploitation Deep Dive

An independent technical article on analyzing heap slab allocators (`kmalloc-512` / `kmalloc-1024`) and building reliable kernel read/write primitives via use-after-free (UAF) vulnerabilities.

## Introduction to SLUB Allocator
The Linux kernel SLUB allocator maintains per-cpu and node slab caches grouped by allocation size objects. When a kernel object is freed without clearing stale pointers, subsequent allocations in the same slab cache can reuse that memory chunk.

## Crafting the Primitive

1. **Trigger Alloc**: Create a target kernel object via `ioctl()`.
2. **Trigger Free**: Close or release the file descriptor while keeping a user-space reference.
3. **Spray Spray**: Allocate user-controlled structures (e.g. `msg_msg` or `pipe_buffer`) to reclaim the slab slot.
4. **Leak & Arbitrary Read/Write**: Corrupt object header structure fields to leak `kaslr` base and overwrite `modprobe_path` or `cred` structures.

```c
// Example slab heap reclamation via msg_msg
struct msgbuf {
    long mtype;
    char mtext[512 - sizeof(long)];
};

int qid = msgget(IPC_PRIVATE, 0666 | IPC_CREAT);
msgsnd(qid, &buf, sizeof(buf.mtext), 0);
```

## Conclusion & Defenses
Modern mitigations such as `AUTOSLAB`, `CONFIG_SLAB_VIRTUAL`, and hardened freelists significantly raise the bar for slab exploitation, requiring cross-cache attacks or synthetic primitives.
