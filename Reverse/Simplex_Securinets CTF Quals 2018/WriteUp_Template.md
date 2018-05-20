# Reference

* 
* https://github.com/acdwas/ctf/blob/master/2018/Securinets%20CTF%20Quals%202018/rev/Service%20Hidden%20in%20the%20Bush/file.py

[//]: <> (文章所涉及到的技术点、WriteUp的链接)



# Title

[//]: <> (题目)

# Content

[//]: <> (WriteUp内容)

Open the binary in IDA, I noticed that it just:

1. check input length;

1. permute input into ch1;

1. compare ch1 with ch2="t_nssiamwp_lsei_hatt{_gaalllF}"

This give me a quick solution.

1. debugging the program using gdb;

1. set a breakpoint at call to strcmp(ch1,ch2);

1. start the program and feed input "ABCDEFGHIJKLMNOabcdefghijklmno"

1. continue excution to breakpoint and check ch1, got "OaNbMcLdKeJfIgHhGiFjEkDlCmBnAo"

perform reverse permutation on ch2:

```Python
   python -c 'print "".join(x for _,x in sorted(zip("OaNbMcLdKeJfIgHhGiFjEkDlCmBnAo","t_nssiamwp_lsei_hatt{_gaalllF}")))'
```

Flag{this_wasnt_simple_at_all}