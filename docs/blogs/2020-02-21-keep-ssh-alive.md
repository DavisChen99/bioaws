# 解决ssh连接服务器掉线问题

> 我们都经历过ssh连上服务器，过段时间没操作，就自动断开了，有时候可能是直接在服务器修改代码，一下子傻了，当然我们不推荐长时间在线修改代码：）
>
> -- D.C

OpenSSH基于安全的理由，如果用户连线到SSH Server后闲置一段时间，SSH Server会在超过特定时间后自动终止SSH连线。

以下方法，个人推荐第2,3种，修改每台服务器真的很烦內~

## 方法1-修改服务器的sshd_config

- 进到ssh文件夹，我们发现有ssh_config和sshd_config两个配置文件。二者区别在于，ssh_config是针对客户端的配置文件，sshd_config则是针对服务端的配置文件。

```bash
$ cd /etc/ssh
$ sudo vi /etc/ssh/sshd_config
```

找到内容，去掉注释并修改如下：

```bash
# 客户端每隔多少秒向服务发送一个心跳数据
ClientAliveInterval 30
# 表示上述多少次心跳无响应之后，会认为Client已经断开。
ClientAliveCountMax 1800
```

保存并重启服务。

```bash
$ service sshd restart
```

## 方法2-修改本机的ssh_config

- 打开本机的ssh_config文件。

```
sudo vi /etc/ssh/ssh_config
```

- 添加内容如下：

```
TCPKeepAlive=yes
ServerAliveInterval 60
ServerAliveCountMax 600
StrictHostKeyChecking no
ForwardAgent yes
Compression yes
```

- 保存，重连ec2。

## 方法3- 利用客户端的反断开功能

- tmux： 终端复用神器! 这个终端里面运行的所有程序，只要你不关电，程序就会一直运行，而且你当你ssh断开再重新连上的时候会接着以前的地方。tmux是linux or Mac，如果是windows，可以用cmder+tmux，或参考[这里](https://github.com/hongwenjun/tmux_for_windows)（感谢大神JJF推荐）
- MobaXterm: edit session - Advanced SSH settings - 选中 _Do not exit after command ends_ 。
- gitbash：修改 _C:\Program Files\Git\etc\ssh\ssh_config_ 。
- secureCRT：会话选项 - 终端 - 反空闲 - 发送NO-OP每xxx秒，设置一个非0值。
- putty：Connection - Seconds between keepalive(0 to turn off)，设置一个非0值。
- iTerm2：profiles - sessions - When idle - send ASCII code.
- XShell：session properties - connection - Keep Alive - Send keep alive message while this session connected. Interval [xxx] sec.
- *以上软件没全部test过，仅基于对软件开发团队的信任 :)*

### 关于tmux

要注意，tmux是安装在服务器上的，你可以理解为screen的进化替代者，所以推荐在ec2的跳板机上安装，再跳到其他机器。

基本概念是：session > window > Pane

```bash
$ sudo yum install tmux
$ vi ~/.~/.tmux.conf
```

写入下列内容，保存退出。

```bash
# Send prefix
set-option -g prefix C-a
unbind-key C-a
bind-key C-a send-prefix

# Use Alt-arrow keys to switch panes
bind -n M-Left select-pane -L
bind -n M-Right select-pane -R
bind -n M-Up select-pane -U
bind -n M-Down select-pane -D

# Shift arrow to switch windows
bind -n S-Left previous-window
bind -n S-Right next-window

# use vim mode to edit
#setw -g mode-keys vi

# Mouse mode
#set -g mouse on
set -g mode-mouse on
set -g mouse-resize-pane on
set -g mouse-select-pane on
set -g mouse-select-window on


# Set easier window split keys
bind-key v split-window -h
bind-key h split-window -v

# Easy config reload
bind-key r source-file ~/.tmux.conf \; display-message "tmux.conf reloaded"
```

设置config之后的常用命令，记住所有tmux开头的命令都是在外面shell里，所有 _prefix_ 开头的都是在session里：

-  _prefix_ : ctrl + a (同时按，放开，再按功能键)
- `tmux new -s <session name> -t <window name>`:新建并命名，懒人直接`tmux new`
- `tmux ls`: 这个命令是在外面的terminal里输入的。当前正常运作中的tmux server会显示（attached）。没有的话就是已关闭，tmux server在后台运行。
-  `prefix + d`: 挂起session,回到外面的shell。
-  `prefix + :`: 进入命令模式，此时可以输入支持的命令，例如kill-server可以关闭tmux服务器，其他命令网上都有。
- `tmux a -t py`: 重新连接名字为py的session。这里的a是attach的意思
- `tmux a`: 如果只有一个session的话，这个是最快的连接方法
-  `prefix + $`: 更名后好让自己知道每一个session是用来做什么的。通常一个session对应一个project
- `tmux kill-session -a -t py`: 在外面输入，删除除了py以外的所有session
- alt+箭头在pane之间切换
- shift+箭头在window之间切换
- 用鼠标点击切换window，pane，调整pane的大小
- 方便切分pane的。prefix + v 代表竖着切，prefix + h 代表横着切。
- 如果在开着tmux情况下修改了.tmux.conf的设置的话，不用关掉tmux。直接用prefix+r,就能重新加载设置。


vim 编辑命令，装B之路不轻松:

|vi             |emacs |       功能|
|--------------|----|------------|
|vi|             emacs|        功能|
|^|              M-m|          反缩进|
|Escape|         C-g|          清除选定内容|
|Enter|          M-w|          复制选定内容|
|j|              Down|         光标下移|
|h|              Left|         光标左移|
|l|              Right|        光标右移|
|L|               |          光标移到尾行|
|M|              M-r|          光标移到中间行|
|H|              M-R|          光标移到首行|
|k|              Up|           光标上移|
|d|              C-u|          删除整行|
|D|              C-k|          删除到行末|
|$|              C-e|          移到行尾|
|:数字|              g|            前往指定行|
|C|-d            M-Down|       向下滚动半屏|
|C|-u            M-Up|         向上滚动半屏|
|C|-f            Page down|    下一页|
|w|              M-f|          下一个词|
|p|              C-y|          粘贴|
|C|-b            Page up|      上一页|
|b|              M-b|          上一个词|
|q  |            Escape|       退出|
|C|-Down or J    C-Down|       向下翻|
|C|-Up or K      C-Up|         向下翻|
|n |             n|            继续搜索|
|?|              C-r|          向前搜索|
|/|              C-s|          向后搜索|
|0|              C-a|          移到行首|
|Space|          C-Space|      开始选中|
|               |C-t|          字符调序|


> Always ask yourself lonely: what's the fact?
