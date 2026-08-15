---
title: "Not a Red Herring"
pubDate: "2026-04-04"
updatedDate: "2026-04-04"
event: "sillyctf-2"
author: ""
score: ""
description: |
  > I promise it's not [https://shorturl.at/pZEPE](https://shorturl.at/pZEPE)

tags: ["rev"]
---

# Not a Red Herring — sillyctf-2 (rev)

—
I promise it's not [https://shorturl.at/pZEPE](https://shorturl.at/pZEPE)

—

just unzip it

ExampleMod.class
ExampleMod$1.class
ExampleMod$2.class
ExampleMod$ClientModEvents.class
Config.class

there are few class

then just javap

SECRET_KEY = "The_Key"
ExampleMod$2 stores an encrypted_flag int array of 27 numbers

Decompile the class files
