断点的删除与断点的设置同样的重要。删除断点的命令有两个:
delete
用法：delete [breakpoints num] [range...]
delete可删除单个断点，也可删除一个断点的集合，这个集合用连续的断点号来描述。
例如：
delete 5
delete 1-10

clear
用法:clear 
    删除所在行的多有断点。
    clear location
clear 删除所选定的环境中所有的断点
clear location location描述具体的断点。
例如：
clear list_insert         //删除函数的所有断点
clear list.c:list_delet   //删除文件：函数的所有断点
clear 12                  //删除行号的所有断点
clear list.c:12           //删除文件：行号的所有断点

clear 删除断点是基于行的，不是把所有的断点都删除。