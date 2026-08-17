---
title: "lactf-26 — smol cats (crypto)"
pubDate: "2026-02-09"
updatedDate: "2026-02-09"
event: "lactf-26"
author: "Level"
score: ""
description: |
  My cat walked across my keyboard and made this RSA implementation, encrypting the location of the treats they stole from me! However, they already got fed twice today, and are already overweight and needs to lose some weight, so I cannot let them eat more treats. Can you defeat my cat's encryption so I can find their secret stash of treats and keep my cat from overeating?

  nc chall.lac.tf 31225
tags: ["crypto"]
---

![Smoll cats - Screenshot](./image.png)

cat the flag text file inside the zip:
`lactf{wHY_aR3_tH3_c4T5_S0_5M0lL_4nD_R0uNd}`
![Smoll cats - Screenshot](./image_1.png)

Terminal output:

```bash
proof of work:
curl -sSfL https://pwn.red/pow | sh -s s.AAA6mA==.Dt3sJFuBAX7YO4gsKDVTig==
solution: s.f+3zeHXexWEpay/gt6CYCyJUJzhy1qkCPVWrLcxv51SC87Uf0GLzUXo8jtyK7I50mcN1DvnyQowXWsYwO6Gwqb6yjykPE/2Rp9J/GNvkIYcMpQMTH7xS4pSc1fYewD1i0i2D6aulfNG0SfTG/OHYocyT3rT+DppMAq4CuTIOzUQuwRFV9+H8xaaUwGRZsuLmI0IF76r8E557p/yCE1GZSw==
  /_/\
 ( o.o ) ^ <
meow Welcome to my cat cafe!
I'm a hungry kitty and I've hidden my treats in a secret place.
I will let you know where I hid them if you can defeat my encryption >.<
I encrypted the number of treats I want with RSA... but my paws are small,
so I used tiny primes. purrrrr

n = 833089423380393996535354065979753699609993609727980884069173
e = 65537
c = 416328151395027680566349936881408333050402980480268361321216mrrrow? How many treats do I want? 540488950358328632426884249065550069626409123190918240775460PURRRRRR You got it right! You may pet me now.
Here's your reward, human:
lactf{sm0l_pr1m3s_4r3_n0t_s3cur3}

```

Solution:

```python
sage: n = 833089423380393996535354065979753699609993609727980884069173
....: e = 65537
....: c = 416328151395027680566349936881408333050402980480268361321216
sage: factor(n)
864240992622568965373716866117 * 963954996918574224996877816369
sage: p, q = n.factor()[0][0], n.factor()[1][0]
sage: phi = (p - 1) * (q - 1)
sage: d = inverse_mod(e, phi)
sage: d
311564791904625735921411235746508904797859071285484965635713
sage: m = power_mod(c, d, n)
sage: m
540488950358328632426884249065550069626409123190918240775460

```

The main thing is that whenever u use a n that is small enough (200 bits in this case) you can use tools like sage (there are other means to do it mathematically)
