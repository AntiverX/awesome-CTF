# Reference

[//]: <> (文章所涉及到的技术点、WriteUp的链接)

* https://www.da.vidbuchanan.co.uk/blog/HITB-XCTF-2018-babypwn.html
* https://nandynarwhals.org/hitbgsecquals2018-babypwn/
* https://fbesnard.com/2018/04/13/HITB-XCTF-Quals-2018-babypwn/

# Title

[//]: <> (题目)

babypwn

nc 47.75.182.113 9999

# Content

[//]: <> (WriteUp内容)


HITB-XCTF GSEC 2018 Quals: babypwn - Blind Format String Exploitation

The only information provided with this challenge was an IP address and port number. No binaries to download! Of course, my first idea was to use netcat to see what it did.

```
$ nc 47.75.182.113 9999
hello
hello
%08x
00000000
```

