# [TIPS] 解决ssh连接EC2总是掉的问题

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

## 方法3- 利用客户端的反断开功能（windows）

- MobaXterm: edit session - Advanced SSH settings - 选中 _Do not exit after command ends_ 。
- gitbash：修改 _C:\Program Files\Git\etc\ssh\ssh_config_ 。
- secureCRT：会话选项 - 终端 - 反空闲 - 发送NO-OP每xxx秒，设置一个非0值。
- putty：Connection - Seconds between keepalive(0 to turn off)，设置一个非0值。
- iTerm2：profiles - sessions - When idle - send ASCII code.
- XShell：session properties - connection - Keep Alive - Send keep alive message while this session connected. Interval [xxx] sec.
- *以上软件没全部test过，仅基于对软件开发团队的信任 :)*




> Always ask yourself lonely: what's the fact?
