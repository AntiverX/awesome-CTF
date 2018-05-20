# Reference

[//]: <> (文章所涉及到的技术点、WriteUp的链接)

https://6l0ry.github.io/zh-tw/xiomaractf-2018/#more

https://www.pwndiary.com/write-ups/xiomara-ctf-2018-giveaway-write-up-crypto150/

# Title

[//]: <> (题目)

Hey! We at Xiomara would love to giveaway the flag to you. But, we can't now, because someone just stole it from us and tried sending it to our rival, Jack. Our super strong web guy here came to the rescue and intercepted it on the way, but found that it was RSA encrypted! You are our crypto guy now. So, decrypt the message and as we promised, the flag is yours!

# Content

[//]: <> (WriteUp内容)

Let’s start with looking at the public key.
```
2
3
$ cat Jacks_public_key 
e = 3
n = 481198641867289038243532927701020249905433964052522187774270437592775342143784702291483427578470414194602731404343532513840453569385856109993166637836189117235549985093499643724363002153995995953731212190003813128852867940536928597102669895224512199695772684398151784349020282852823384810308548307944122748283
```

We see that public exponential is too low. If we call plain message as m and ciphertext as c, this is how c is generated.

```
c = pow(m, e) % n
```

We can write this equation as follows:

```
pow(m, e) = c + n * k
```

If the message is longer, we get larger k. However, if the message is short, we might brute force the value of k and decrypt the message.

Here is the code that brute forces k and decrypts the message.

```python
#!/usr/bin/env python
import gmpy
from libnum import *
 
n = 481198641867289038243532927701020249905433964052522187774270437592775342143784702291483427578470414194602731404343532513840453569385856109993166637836189117235549985093499643724363002153995995953731212190003813128852867940536928597102669895224512199695772684398151784349020282852823384810308548307944122748283
e = 3
 
c = 2039130155866184490894181588949291569587424373754875837330412835527276040280846677481047284126316137541961805207979583672570357348995401556991229785828117383170279052532972654304372432603436204862621797
while True:
    m = gmpy.root(c, e)[0]
    if pow(m, e, n) == c:
        print n2s(m)
        break
    c += N
```

Let’s run the script and get the flag.

```
$ python decrypt.py
xiomara{4y3_4y3_cryp70_6uy!}
```

Here is the flag xiomara{4y3_4y3_cryp70_6uy!}.