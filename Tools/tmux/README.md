# tmux

## 安装
```
sudo apt-get install tmux
```

## 使用

命令|解释
-|-
tmux|打开tumx
ctrl + b c|创建一个窗口
ctrl + b "|上下分屏
ctrl + b %|左右分屏
ctrl + b o|切换面板
ctrl + b x|关闭一个面板
ctrl + b d|脱离当前会话；这样可以暂时返回Shell界面，输入tmux attach能够重新进入之前的会话
ctrl + b space|上下分屏与左右分屏切换
ctrl + b q|显示面板编号
Ctrl + b &|关闭当前窗口
ctrl + b Ctrl+方向键|以1个单元格为单位移动边缘以调整当前面板大小
ctrl + b Alt+方向键|以5个单元格为单位移动边缘以调整当前面板大小
ctrl + b 方向键|移动光标选择对应面板
ctrl + b Alt + o |逆时针旋转当前窗口的面板
ctrl + b Ctrl+o|顺时针旋转当前窗口的面板
ctrl + b ,|重命名当前窗口；这样便于识别
## 其他

! 将当前面板置于新窗口,即新建一个窗口,其中仅包含当前面板

空格键 可以在默认面板布局中切换，试试就知道了

{ 向前置换当前面板

} 向后置换当前面板


