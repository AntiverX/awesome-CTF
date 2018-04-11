# Reference

[//]: <> (文章所涉及到的技术点、WriteUp的链接)

* https://devcraft.io/2018/04/08/sunshine-ctf-2018.html#order-matters
* https://ctftime.org/writeup/9558

# Title

[//]: <> (题目)

The vault to access this armory is protected with some weird password algorithm. Can you gain access?

Author: Winyl

Hint: The password should be a string of unique numbers (eq. 1 2 11 12 = 01021112)

Update 2018-04-06 19:15 UTC: Increased point value from 250 -> 350. Update 2018-04-07 00:02 UTC: Added hint!

# Content

[//]: <> (WriteUp内容)

The binary reads a password, and then depending on the numbers will perform one of 15 operations. I started trying to solve this with angr, but that wasn’t working at. Taking another look at the disassembly I saw that all the steps were getting thier values like this:

```C
long p06()
{
  return strtol("51563969", 0, 16);
}
```

The constansts were very suspicious, as the were all in the ascii range. Sure enough, converting them to text revealed that they were base64:

```Python
#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from pwn import *

bits = [
  b64d(unhex("58335249")),
  b64d(unhex("58306c45")),
  b64d(unhex("5a314e66")),
  b64d(unhex("63335675")),
  b64d(unhex("58335177")),
  b64d(unhex("51563969")),
  b64d(unhex("4e484a45")),
  b64d(unhex("66513d3d")),
  b64d(unhex("4d313935")),
  b64d(unhex("59544578")),
  b64d(unhex("4d313943")),
  b64d(unhex("4d486c7a")),
  b64d(unhex("6532315a")),
  b64d(unhex("5831526f")),
  b64d(unhex("556a4675")),
]

for i, bit in enumerate(bits):
  print "{} - {}".format(i+1, bit)
```

Running it:
```
$ ./solv.py
1 - _tH
2 - _ID
3 - gS_
4 - sun
5 - _t0
6 - A_b
7 - 4rD
8 - }
9 - 3_y
10 - a11
11 - 3_B
12 - 0ys
13 - {mY
14 - _Th
15 - R1n
```

So now the name makes sense, we have to find the correct order of to produce the flag. After a bit of manual swapping we we end up wit h the password ```041302061503101411120501090708``` and the flag ```sun{mY_IDA_bR1ngS_a11_Th3_B0ys_t0_tH3_y4rD}```
