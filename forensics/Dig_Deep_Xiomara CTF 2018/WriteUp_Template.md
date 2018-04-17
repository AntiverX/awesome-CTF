# Reference

[//]: <> (文章所涉及到的技术点、WriteUp的链接)

* https://www.pwndiary.com/write-ups/xiomara-ctf-2018-dig_deep-write-up-forensics150/
* http://www.aperikube.fr/docs/xiomara_2018_dig_deep/

# Title

[//]: <> (题目)



# Content

[//]: <> (WriteUp内容)


After extracting the file from the archive, I checked its signature first.

```
$ file private.dd
private.dd: DOS/MBR boot sector, code offset 0x3c+2, OEM-ID "mkfs.fat", sectors/cluster 4, root entries 512, Media descriptor 0xf8, sectors/FAT 200, sectors/track 32, heads 64, sectors 204800 (volumes > 32 MB), serial number 0x2e594bed, unlabeled, FAT (16 bit)
```

It is a DOS/MBR boot sector file. Since the challenge name is Dig_Deep, I used foremost directly instead of mounting the boot sector.

```
$ foremost private.dd
$ cd output
$ ls
audit.txt  gif  jpg  png  zip
$ ls zip
00037165.zip
```

Yay, we now have a git repository. Let’s check its history.

```
$ cd .git
$ git log --patch | grep xiomara
Author: lolzzz <fakemail@xiomara.com>
Author: lolzzz <fakemail@xiomara.com>
-xiomara{wow_autopsy_&_git_is_cool}
Author: lolzzz <fakemail@xiomara.com>
-xiomara{} well this is our flag format
+xiomara{wow_autopsy_&_git_is_cool}
Author: lolzzz <fakemail@xiomara.com>
 xiomara{} well this is our flag format
Author: lolzzz <fakemail@xiomara.com>
+xiomara{} well this is our flag format
```

Here we got the flag xiomara{wow_autopsy_&_git_is_cool}.