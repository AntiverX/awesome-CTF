# Reference

[//]: <> (文章所涉及到的技术点、WriteUp的链接)

* https://ctftime.org/writeup/9619
* https://devcraft.io/2018/04/08/sunshine-ctf-2018.html#source-protection
* https://github.com/countercept/python-exe-unpacker

# Title

[//]: <> (题目)

Source Protection

People said I shouldn't use Python to write my password vault because they would be able to read my source code, but they underestimated how smart I am. In fact, I'm so confident in my source code protection that I'm going to upload my password vault and challeng a bunch of nerds to hack it. Good luck :)

Author: hackucf_dmaria

passwords.exe

# Content

[//]: <> (WriteUp内容)


The description suggest that the program was written in python then compiled. This leaves 2 methods of compilation, Py2Exe and PyInstaller. Upon messing around, I found out that it was not compiled using Py2Exe. I proceded to use a PyInstaller extractor to extract the files. Download the extractor here: [PyInstxtractor](https://sourceforge.net/projects/pyinstallerextractor/files/latest/download)

Extract the files using the command python pyinstxtractor.py passwords.exe

Next, change directory into the extracted folder and notice that there is a passwords file.

Retrieve the flag using cat passwords | grep sun

sun{py1n574ll3r_15n7_50urc3_pr073c710n}