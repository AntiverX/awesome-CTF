# Reference

[//]: <> (文章所涉及到的技术点、WriteUp的链接)

* https://tipi-hack.github.io/2018/04/01/quals-NDH-18-man-in-the-mirror.html
* https://ctftime.org/writeup/9535
* https://ctftime.org/writeup/9412
# Title

[//]: <> (题目)

Hey, mickey ! - Give me your IP adress ! - I'll send you what you're looking for. - Stay tuned on 5555 ! http://maninthemirror.challs.malice.fr

![](Resource/1_1.png)

# Content

[//]: <> (WriteUp内容)

Solves: 10 / Points: 500

## Challenge description

We were provided an URL leading to a single page website with a form and the following message:
```
Hey, mickey ! - Give me your IP adress ! - I’ll send you what you’re looking for. - Stay tuned on 5555 !
```

## Challenge resolution

Let’s start a listener on port 5555 and submit our IP address:
```
# nc -lvp 5555
listening on [any] 5555 ...
Warning: forward host lookup failed for 51-15-185-101.rev.poneytelecom.eu: Unknown host
connect to [10.8.20.207] from 51-15-185-101.rev.poneytelecom.eu [51.15.185.101] 39920
SSH-2.0-OpenSSH_7.4p1 Debian-10+deb9u3
```

The server tries to initiate an SSH connection, our first idea was to set up a small SSH honeypot with Cowrie to spy on the user. It works great but only gives half of the flag and no additional information. After many unsuccessful attempts (and the end of the CTF :( ) we decided to take a look at the user’s public key.

To do so, we used the Paramiko Python module to log connection information:
```python
#!/usr/bin/env python
import logging
import socket
import sys
import threading
from binascii import hexlify
import paramiko

logging.basicConfig()
logger = logging.getLogger()

if len(sys.argv) != 2:
    print "Need private host RSA key as argument."
    sys.exit(1)

host_key = paramiko.RSAKey(filename=sys.argv[1])


class Server(paramiko.ServerInterface):
    def __init__(self):
        self.event = threading.Event()

    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED

    def check_auth_password(self, username, password):
        print('Auth attempt for user %s with password: %s ' % (username, password))
        return paramiko.AUTH_SUCCESSFUL

    def check_auth_publickey(self, username, key):
        print('Auth attempt for user %s with key: %s' % (username, key.get_base64()))
        return paramiko.AUTH_SUCCESSFUL

    def get_allowed_auths(self, username):
        return 'publickey,password'

    def check_channel_exec_request(self, channel, command):
        # This is the command we need to parse
        print command
        self.event.set()
        return True


def listener():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', 5555))

    sock.listen(100)
    client, addr = sock.accept()

    t = paramiko.Transport(client)
    t.set_gss_host(socket.getfqdn(""))
    t.load_server_moduli()
    t.add_server_key(host_key)
    server = Server()
    t.start_server(server=server)

    # Wait 30 seconds for a command
    server.event.wait(30)
    t.close()


while True:
    try:
        listener()
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as exc:
        logger.error(exc)
```

We can run the server and trigger a new connection:
```
 python serv2.py test_rsa.key
Auth attempt for user mickey with key: AAAAB3NzaC1yc2EAAACBAVcIniIfR3tkfO/0E7W/lri2ec4WGca6CH7nOm8PqV4W+fHSKLSghmOauArZW0DuSDM9zqpXrPBx3QHBoe2x/1Vt25yyzjj99EwtmUefedtU+eRJopFSSKr5UaImhBxx8QqxkCkRGzg8SRaiOnKqXykCC8
tDDjZT0k57BzQPT6z3AAAAgQG1/myKcXWiQhXSDEFULU7Qambs0+kkT+LLcuX7B08sbcvzoG+a5OYziM6QbTZQjtw/nhEHxbt0wAAJe/hi5MWAMRTPOZqg50SaS5lOZnLSGlR+DRGz7b/woF3Wkqdv0ZSTNq7L+o5WtzcffiJdAmHoQlC1gKhI8MqsO0E3Q3SQHQ==
echo NDH{a_WInN3r_15_A_Dr3AMeR > ~/flag_1.txt
```
Well, now we have the public key and first part of the flag. Before doing anything else, we need to convert the public key to PEM format and use OpenSSL to get the modulus and exponent:

```
# ssh-keygen -f public.key -e -m PKCS8 > public.pem
# openssl rsa -pubin -inform PEM -text -noout -in public.pem
Public-Key: (1025 bit)
Modulus:
    01:b5:fe:6c:8a:71:75:a2:42:15:d2:0c:41:54:2d:
    4e:d0:6a:66:ec:d3:e9:24:4f:e2:cb:72:e5:fb:07:
    4f:2c:6d:cb:f3:a0:6f:9a:e4:e6:33:88:ce:90:6d:
    36:50:8e:dc:3f:9e:11:07:c5:bb:74:c0:00:09:7b:
    f8:62:e4:c5:80:31:14:cf:39:9a:a0:e7:44:9a:4b:
    99:4e:66:72:d2:1a:54:7e:0d:11:b3:ed:bf:f0:a0:
    5d:d6:92:a7:6f:d1:94:93:36:ae:cb:fa:8e:56:b7:
    37:1f:7e:22:5d:02:61:e8:42:50:b5:80:a8:48:f0:
    ca:ac:3b:41:37:43:74:90:1d
Exponent:
    01:57:08:9e:22:1f:47:7b:64:7c:ef:f4:13:b5:bf:
    96:b8:b6:79:ce:16:19:c6:ba:08:7e:e7:3a:6f:0f:
    a9:5e:16:f9:f1:d2:28:b4:a0:86:63:9a:b8:0a:d9:
    5b:40:ee:48:33:3d:ce:aa:57:ac:f0:71:dd:01:c1:
    a1:ed:b1:ff:55:6d:db:9c:b2:ce:38:fd:f4:4c:2d:
    99:47:9f:79:db:54:f9:e4:49:a2:91:52:48:aa:f9:
    51:a2:26:84:1c:71:f1:0a:b1:90:29:11:1b:38:3c:
    49:16:a2:3a:72:aa:5f:29:02:0b:cb:43:0e:36:53:
    d2:4e:7b:07:34:0f:4f:ac:f7
```

The key is only 1025 bits long?? Let’s try a Wiener attack in order to get the corresponding private key:

```python
from sage.all import *
from Crypto.PublicKey import RSA
import sys

def factor_rsa_wiener(N, e):
    """Wiener's attack: Factorize the RSA modulus N given the public exponents
    e when d is small.
    Source: https://crypto.stanford.edu/~dabo/papers/RSA-survey.pdf
    CTF: BKP CTF 2016 Bob's Hat
    """
    N = Integer(N)
    e = Integer(e)
    cf = (e / N).continued_fraction().convergents()
    for f in cf:
        k = f.numer()
        d = f.denom()
        if k == 0:
            continue
        phi_N = ((e * d) - 1) / k
        b = -(N - phi_N + 1)
        dis = b ** 2 - 4 * N
        if dis.sign() == 1:
            dis_sqrt = sqrt(dis)
            p = (-b + dis_sqrt) / 2
            q = (-b - dis_sqrt) / 2
            if p.is_integer() and q.is_integer() and (p * q) % N == 0:
                p = p % N
                q = q % N
                if p > q:
                    return (p, q)
                else:
                    return (q, p)

# some message for testing purpose
m=1010101010

# n and e extracted using : openssl rsa -pubin -inform PEM -text -noout -in keyp.pem
n=0x01b5fe6c8a7175a24215d20c41542d4ed06a66ecd3e9244fe2cb72e5fb074f2c6dcbf3a06f9ae4e63388ce906d36508edc3f9e1107c5bb74c000097bf862e4c5803114cf399aa0e7449a4b994e6672d21a547e0d11b3edbff0a05dd692a76fd1949336aecbfa8e56b7371f7e225d0261e84250b580a848f0caac3b41374374901d
e=0x0157089e221f477b647ceff413b5bf96b8b679ce1619c6ba087ee73a6f0fa95e16f9f1d228b4a086639ab80ad95b40ee48333dceaa57acf071dd01c1a1edb1ff556ddb9cb2ce38fdf44c2d99479f79db54f9e449a2915248aaf951a226841c71f10ab19029111b383c4916a23a72aa5f29020bcb430e3653d24e7b07340f4facf7

print("[~] Using Wiener attack to retrieve the private exponent")
p,q = factor_rsa_wiener(n,e)
print("[+] Found p: %d") % p
print("[+] Found q: %d") % q
print("[~] Calculating the private exponent from previous p and q")
phi = (p - 1) * (q - 1)
d = inverse_mod(e, phi)

c = Mod(m, n) ** e
if m != Mod(c, n) ** d:
    print("[!] bad private key, exiting ...")
    sys.exit()
else:
    print("[+] Found private exponent!")

print("[~] Generating PEM private key")
key = RSA.construct((long(n),long(e),long(d)))
print(key.exportKey())
```

We run the script:
```
$ python2 wiener.py

[~] Using Wiener attack to retrieve the private exponent
[+] Found p: 20889245576632215937496060923102635902336468597218301616718124305930809261428763079736436110981840441822764789723011958852494201758313569356745363994791549
[+] Found q: 14723831723094455775085365007141143530544095877112879851235256680184460118386958820268233017983677957272300333838816815589094172676082132570036830797290017
[~] Calculating the private exponent from previous p and q
[+] Found private exponent!
[~] Generating PEM private key
-----BEGIN RSA PRIVATE KEY-----
MIICOgIBAAKBgQG1/myKcXWiQhXSDEFULU7Qambs0+kkT+LLcuX7B08sbcvzoG+a
5OYziM6QbTZQjtw/nhEHxbt0wAAJe/hi5MWAMRTPOZqg50SaS5lOZnLSGlR+DRGz
7b/woF3Wkqdv0ZSTNq7L+o5WtzcffiJdAmHoQlC1gKhI8MqsO0E3Q3SQHQKBgQFX
CJ4iH0d7ZHzv9BO1v5a4tnnOFhnGugh+5zpvD6leFvnx0ii0oIZjmrgK2VtA7kgz
Pc6qV6zwcd0BwaHtsf9Vbducss44/fRMLZlHn3nbVPnkSaKRUkiq+VGiJoQccfEK
sZApERs4PEkWojpyql8pAgvLQw42U9JOewc0D0+s9wIgGRbivJwJdSlS8x7NB4J4
xbhJWKhljWHJMWnga0qoIMcCQQEZIJceQq+jIJJ8YsxEvjwWVOtkPt8yVmNt2uNN
+OA8t/mj13mnCI0PXSlHhGOiGzHyF/wvwsbWNyZTvdxbX9ohAkEBjtiBZmqmDb0B
UXcnBU9fmMeSARSzTvpcYlFXMy/ZQpFFOWchEOZtxjT6Nza8nkG7ePNX6MaGVE6Y
xoZdVRFOfQIgGRbivJwJdSlS8x7NB4J4xbhJWKhljWHJMWnga0qoIMcCIBkW4ryc
CXUpUvMezQeCeMW4SVioZY1hyTFp4GtKqCDHAkEAvxQ93dEo5hEGiTZ1IVXR+TmL
VgyFOnIZnCWfXAhz6UQkk0MJ+yCUICzqQZcmpUmlNMumA36w75lZmcexL22zeA==
-----END RSA PRIVATE KEY-----
```

Now that we have the private key, we can connect to the server on port 2222 (“mirror image” of 5555 (otherwise nmap is a great tool)) and grab the second part of the flag:

```
# ssh -i private.pem mickey@maninthemirror.challs.malice.fr -p 2222
Linux 24b0bd880e30 4.9.0-3-amd64 #1 SMP Debian 4.9.30-2+deb9u5 (2017-09-19) x86_64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Sun Apr  1 15:23:24 2018 from 192.168.32.3
-bash: warning: setlocale: LC_ALL: cannot change locale (en_US.UTF-8)
mickey@24b0bd880e30:~$ ls
flag_2.txt
mickey@24b0bd880e30:~$ cat flag_2.txt
_Wh0_NeV3R_gIve5_uP}
```