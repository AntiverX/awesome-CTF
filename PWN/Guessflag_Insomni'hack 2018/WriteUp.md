# Reference

* https://inshallhack.org/guessflag_insomnihack/



# Title

Guessflag was a warmup pwn at Insomni'hack 2018. It was a fairly easy challenge, but we struggled a lot on small details.
# Content

## The challenge
We were given ssh access to a remote server, and the challenge was in ``` /home/flag ``` there. There we could find a shared lib (```dowin.so```), the main binary (```guessflag```), and a text file (```flag.txt```).

We could see that ```guessflag``` was ```setgid``` and that the owner of both the ```flag.txt``` file and the ```guessflag``` binary was part of the group "flag".

```
user1@insomniak:/home/flag$ ls -al
total 32
drwxr-xr-x  2 root root  4096 Mar 26 13:18 .
drwxr-xr-x 12 root root 4096 Mar 26 12:50 ..
-rwxr-xr-x  1 root root  7512 Mar 26 12:50 dowin.so
-rwxr-sr-x  1 root flag  8520 Mar 26 12:51 guessflag
-rw-r-----  1 root flag   262 Mar 26 13:18 flag.txt
```

With this information, we knew that we'd probably have to exploit the ```guessflag``` binary to run commands as a member of the "flag" group in order to read ```flag.txt```, which most likely contains the flag.

## Analysis
Let's start with some analysis of the binary.

First we look at the output of the ```file``` command:

```
user1@insomniak:/home/flag$ file guessflag                                                                                                                      
guessflag: setgid ELF 64-bit LSB shared object, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 2.6.32, not stripped
```

It tells us that ```guessflag``` is compiled as a dynamic binary, which means that it relies on the ```libc``` of the remote server for standard functions like ```printf``` et al.! We could make it use our own standard function using [LD_PRELOAD](https://www.goldsborough.me/c/low-level/kernel/2016/08/29/16-48-53-the_-ld_preload-_trick/) trick, but from our little experience, we know that LD_PRELOAD is ignored when the binary is setuid or setgid, which is the case here.

So let's move on and look at the output of ```ltrace```.

```
user1@insomniak:/home/flag$ ltrace ./guessflag
puts("Can you guess the flag ?"Can you guess the flag ?)                 = 25
+++ exited (status 255) +++
```

Nothing fancy here, let's try with an argument.

```
user1@insomniak:/home/flag$ ltrace ./guessflag arg
puts("Can you guess the flag ?"Can you guess the flag ?)                 = 25
getenv("CHECK_PATH")                                                     = nil
snprintf("(null)/dowin.so", 1024, "%s/dowin.so", nil)                    = 15
dlopen("(null)/dowin.so", 1)                                             = 0
+++ exited (status 255) +++
```

Uuh! Looks like it first checks if we passed an argument, and if so, tries to get the content of the environment variable ```CHECK_PATH```.

Let's try to set this variable :

```
user1@insomniak:/home/flag$ CHECK_PATH=test ltrace ./guessflag arg
puts("Can you guess the flag ?"Can you guess the flag ?)                 = 25
getenv("CHECK_PATH")                                                     = "test"
snprintf("test/dowin.so", 1024, "%s/dowin.so", "test")                   = 13
dlopen("test/dowin.so", 1)                                               = 0
+++ exited (status 255) +++
```

Alright, so it looks like it appends the content of CHECK_PATH to the string "/dowin.so" and then tries to use ```dlopen``` on it. This means that if we set the CHECK_PATH variable to something like /tmp/pld and create our own dowin.so in this directory, it will load it !