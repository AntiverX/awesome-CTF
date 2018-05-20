https://www.ichunqiu.com/writeup/detail/1165

![](Resource/1521013642_659899.jpg)

peid查一下，发现为 .net

于是用net reflector打开，查看一下有什么函数
![](Resource/1521013800_659899.jpg)
然后就很清楚了，base64解码，即可得到flag