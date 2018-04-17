# Reference

[//]: <> (文章所涉及到的技术点、WriteUp的链接)

* https://github.com/antihorsey/ctf-writeups/blob/master/sunshine-2018/LogSearch/logsearch.py
* https://github.com/phieulang1993/ctf-writeups/blob/master/2018/sunshinectf/logsearch/logsearch.py
# Title

[//]: <> (题目)

Log Search

Log Search 150 This program searches through IRC logs. See if you can find anything else inside!

nc chal1.sunshinectf.org 20008

Author: hackucf_kcolley

Files: logsearch logsearch.c libpwnableharness32.so

# Content

[//]: <> (WriteUp内容)


Pretty straightforward printf vulnerability. pwntools will do the heavy lifting for us. The main key to this one is to do it efficiently.

We could put in a lot of effort and get full execution control. But all we need is the flag. Studying the log search function provides us with a quicker path to the flag -- overwrite the log filename with flag.txt, overwrite strstr with printf, and instead of searching the log for a search query, it will print every line from the flag.

One thing to watch out for: GOT entries are pointers to executable code and PLT entries are executable code. You can't overwrite a GOT entry with a pointer to a GOT entry because that makes it a pointer to a pointer to executable code. Overwriting it with an entry to another PLT entry makes it a pointer to executable code even though it will take you through the PLT/GOT twice. In this instance, execution will look like: strstr@plt -> strstr@got -> printf@plt -> printf@got -> printf@libc.