# 善物 - python脚本查询AWS EC2 价格

> 主要是闲的D疼。。。
>
> -- D.C



### 离线模式（默认）

- help 信息

```bash
$  python ec2liveprice.py -h
Usage: ec2liveprice.py [options] InstanceType

Options:
  -h, --help            show this help message and exit
  -m MODE, --mode=MODE  off/on/update (off by default)
  -t TYPE, --type=TYPE  od/do/ri/dri/cri/cdri (ri by default)
  -s OS, --os=OS        li/win/su/rh/wsqs/wsqw/wsqe (li by default)
  -r REGION, --region=REGION
                        bjs/zhy (zhy by default)
  -p                    print abbrevs to stdout
```

- p选项查看缩写含义：

```bash
$  python ec2liveprice.py -p

Abbreviations:
bjs <---> 北京区域
zhy <---> 宁夏区域
od <---> 按需实例
do <---> 专用按需实例
ri <---> 预留实例
dri <---> 专业预留实例
cri <---> 可转换实例
cdri <---> 可转换专用预留实例
li <---> EC2 Linux
win <---> EC2 Windows
su <---> EC2 SUSE
rh <---> EC2 RHEL
wsqs <---> 采用 SQL Standard 的 EC2 Windows
wsqw <---> 采用 SQL Web 的 EC2 Windows
wssqe <---> 采用 SQL Server Enterprise 的 EC2 Windows
```

- 默认选项：宁夏区(zhy) - Linux系统(li) - 预留实例（ri）

```bash
$ python ec2liveprice.py m5.xl
[offline mode]

# 宁夏区域 - EC2 Linux - 预留实例
实例类型        期限    产品类型        预付价格（人民币）      使用价格（人民币）      月度成本（人民币）      有效RI率        与OD相比的成本节省      OD价格（人民币）/每小时
m5.xlarge       1 年    无预付费用      0       0.421   307.33  0.421   69%     1.356
m5.xlarge       1 年    预付部分费用    1755    0.2     146     0.4     71%     1.356
m5.xlarge       1 年    预付全部费用    3441    0       0       0.393   71%     1.356
m5.xlarge       3 年    无预付费用      0       0.26    189.8   0.26    81%     1.356
m5.xlarge       3 年    预付部分费用    3163    0.12    87.6    0.24    82%     1.356
m5.xlarge       3 年    预付全部费用    5947    0       0       0.226   83%     1.356
```

- 查询多个： 宁夏区（zhy） - Linux系统(li) - 预留实例（ri）

```bash
$  python ec2liveprice.py m5.xl r5.xl c5.xl
[offline mode]

# 宁夏区域 - EC2 Linux - 预留实例
实例类型        期限    产品类型        预付价格（人民币）      使用价格（人民币）      月度成本（人民币）      有效RI率        与OD相比的成本节省      OD价格（人民币）/每小时
m5.xlarge       1 年    无预付费用      0       0.421   307.33  0.421   69%     1.356
m5.xlarge       1 年    预付部分费用    1755    0.2     146     0.4     71%     1.356
m5.xlarge       1 年    预付全部费用    3441    0       0       0.393   71%     1.356
m5.xlarge       3 年    无预付费用      0       0.26    189.8   0.26    81%     1.356
m5.xlarge       3 年    预付部分费用    3163    0.12    87.6    0.24    82%     1.356
m5.xlarge       3 年    预付全部费用    5947    0       0       0.226   83%     1.356
c5.xlarge       1 年    无预付费用      0       0.35    255.5   0.35    65%     0.986
c5.xlarge       1 年    预付部分费用    1458    0.166   121.18  0.332   66%     0.986
c5.xlarge       1 年    预付全部费用    2858    0       0       0.326   67%     0.986
c5.xlarge       3 年    无预付费用      0       0.232   169.36  0.232   76%     0.986
c5.xlarge       3 年    预付部分费用    2824    0.107   78.11   0.214   78%     0.986
c5.xlarge       3 年    预付全部费用    5309    0       0       0.202   80%     0.986
r5.xlarge       1 年    无预付费用      0       0.55    401.5   0.55    69%     1.766
r5.xlarge       1 年    预付部分费用    2294    0.262   191.26  0.524   70%     1.766
r5.xlarge       1 年    预付全部费用    4496    0       0       0.513   71%     1.766
r5.xlarge       3 年    无预付费用      0       0.339   247.47  0.339   81%     1.766
r5.xlarge       3 年    预付部分费用    4122    0.157   114.61  0.314   82%     1.766
r5.xlarge       3 年    预付全部费用    7750    0       0       0.295   83%     1.766
```

- 查询： 北京区（bjs） - windows(win) - 按需实例(od)

```bash
$  python ec2liveprice.py -r bjs -t od -s win m5.xl
[offline mode]

# 北京区域 - EC2 Windows - 按需实例
实例类型        vCPU    ECU     内存    存储    OD价格（人民币）/每小时
m5.xlarge       4       N/A     16      仅限 EBS        3.286
```

- 

### 在线模式（需联网，现爬现查）

- 更新全部价格库: `-m update`

```bash
$ python ec2liveprice.py -m update
[update mode]
--2021-01-26 17:15:36--  https://www.amazonaws.cn/ec2/pricing/ec2-linux-pricing/
Resolving www.amazonaws.cn (www.amazonaws.cn)... 54.222.5.185
Connecting to www.amazonaws.cn (www.amazonaws.cn)|54.222.5.185|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: unspecified [text/html]
Saving to: 'C:/Users/dir/to/ec2price//ec2_linux.html'

C:/Users/dir/to/ec2price//ec2     [                <=>                                                        ]   2.69M   799KB/s    in 3.6s

2021-01-26 17:15:40 (774 KB/s) - 'C:/Users/dir/to/ec2price//ec2_linux.html' saved [2818252]

updating... C:\Users\dir\to\ec2price\\ec2_linux_0.txt
> updated :)
updating... C:\Users\dir\to\ec2price\\ec2_linux_1.txt
> updated :)
updating... C:\Users\dir\to\ec2price\\ec2_linux_2.txt
> updated :)
updating... C:\Users\dir\to\ec2price\\ec2_linux_3.txt
> updated :)
updating... C:\Users\dir\to\ec2price\\ec2_linux_4.txt
> updated :)
updating... C:\Users\dir\to\ec2price\\ec2_linux_5.txt
> updated :)
updating... C:\Users\dir\to\ec2price\\ec2_linux_6.txt
> updated :)
updating... C:\Users\dir\to\ec2price\\ec2_linux_7.txt
> updated :)
updating... C:\Users\dir\to\ec2price\\ec2_linux_8.txt
> updated :)
updating... C:\Users\dir\to\ec2price\\ec2_linux_9.txt
> updated :)
updating... C:\Users\dir\to\ec2price\\ec2_linux_10.txt
> updated :)
updating... C:\Users\dir\to\ec2price\\ec2_linux_11.txt
> updated :)
--2021-01-26 17:15:44--  https://www.amazonaws.cn/ec2/pricing/ec2-windows-pricing/
Resolving www.amazonaws.cn (www.amazonaws.cn)... 54.222.5.185
Connecting to www.amazonaws.cn (www.amazonaws.cn)|54.222.5.185|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: unspecified [text/html]
Saving to: 'C:/Users/dir/to/ec2price//ec2_win.html'

C:/Users/dir/to/ec2price//ec2     [               <=>                                                         ]   2.41M   789KB/s    in 3.1s

2021-01-26 17:15:47 (789 KB/s) - 'C:/Users/dir/to/ec2price//ec2_win.html' saved [2528413]
...
...
```

- 在线模式：宁夏区(zhy) - Linux系统(li) - 预留实例（ri）

```
$ python ec2liveprice.py -m on m5.x
[online mode]
--2021-01-26 17:23:30--  https://www.amazonaws.cn/ec2/pricing/ec2-linux-pricing/
Resolving www.amazonaws.cn (www.amazonaws.cn)... 54.222.4.224
Connecting to www.amazonaws.cn (www.amazonaws.cn)|54.222.4.224|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: unspecified [text/html]
Saving to: 'C:/Users/dir/to/ec2price//ec2_linux.html'

C:/Users/dir/to/ec2price//ec2     [                 <=>                                                       ]   2.69M   833KB/s    in 3.4s

2021-01-26 17:23:34 (805 KB/s) - 'C:/Users/dir/to/ec2price//ec2_linux.html' saved [2818252]

> updating... C:\Users\dir\to\ec2price\\ec2_linux_2.txt
> updated :)

# 宁夏区域 - EC2 Linux - 预留实例
实例类型        期限    产品类型        预付价格（人民币）      使用价格（人民币）      月度成本（人民币）      有效RI率        与OD相比的成本节省      OD价格（人民币）/每小时
m5.xlarge       1 年    无预付费用      0       0.421   307.33  0.421   69%     1.356
m5.xlarge       1 年    预付部分费用    1755    0.2     146     0.4     71%     1.356
m5.xlarge       1 年    预付全部费用    3441    0       0       0.393   71%     1.356
m5.xlarge       3 年    无预付费用      0       0.26    189.8   0.26    81%     1.356
m5.xlarge       3 年    预付部分费用    3163    0.12    87.6    0.24    82%     1.356
m5.xlarge       3 年    预付全部费用    5947    0       0       0.226   83%     1.356
```

- 其他选项类似，只是多了个 `-m on`

### 说说安装

- 需要python包： `io`,`sys`,`os`,`re`,`optparse`,`bs4`。 一般python都自带的，除了 `bs4`。

版本：

```bash
$ python --version
Python 3.8.1
```

- copy 代码另存为文件名 _ec2liveprice.py_：

[代码在此](../img/codes/ec2livepirce.py)

- 记事本打开修改以下路径为自己的路径,这个路径会用来放置爬下来的价格文件，共91个文件：

```python
# NEED CHANGE to the dir you want to put the crawled data

#########################################################
if mysystem == 'win':                                   #
    pathdir= r'C:\dir\to\mytools\ec2price\\'     # windows 路径规则
else:                                                   #
    pathdir= r'/Users/dir/to/ec2price/'        # 其他linux路径规则
#########################################################  
```

- enjoy ~


> 写完以后架构师告诉我,其实有api可以调用的 -.-。。。