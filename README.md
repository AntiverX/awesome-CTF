# awesome-CTF
## 初始化教程
1. 下载git for windows

>https://git-scm.com/

2. 在github上fork awesome-CTF
>https://github.com/AntiverX/awesome-CTF

3. 在cmd设置git（名字和邮箱都是你的github名字、邮箱）
>git config --global user.name "Your Name"

>git config --global user.email "email@example.com"

>git config --global https.proxy https://127.0.0.1:1080/ (可选项，可以使用代理加速仓库同步)

4. 克隆仓库到本地（Your_name是自己的账号，为了保存到合适的位置，可以先CD到其他目录。不然默认是你的用户目录）
>git clone https://github.com/Your_Name/awsome-CTF.git 

## 日常使用教程
添加所有的有改动的文件
>git add . 

提交所有的文件到本地仓库
>git commit

提交所有的变更到github仓库，使用该命令后会弹出个vim让你填写变更信息，简要说明提交的变更内容即可
>git push

如需提交变更到主分支，请到github上pull request

## CTF格式
1. 一道题目的目录命名为：题目名_出题方，如easy_ISCC 2017
2. 目录下包含两个目录，一个名为Source，一个名为Resource；包含一个markdown文件，名为WriteUp.md
    + Source存放题目文件
    + Resource存放markdown中的图片等资源
    + WriteUp.md即为题解


## 注意事项

1. 由于网络问题提交可能不成功，多尝试几次即可
