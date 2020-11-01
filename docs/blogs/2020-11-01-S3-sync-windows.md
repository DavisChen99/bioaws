# windows 定期自动同步数据到S3

> 虽然生物信息一般都会用Linux系统来存储数据和运算，但是还是有些同学有从windows同步数据到AWS S3的需求，比如实验室的仪器配套的计算机上的重要数据，比如存储影像数据的win服务器等，本文就简要介绍下如何利用windows自带的定时任务配合一个小脚本实现自动同步数据。
>
> -- D.C

_名词解释：S3 --- AWS上的对象存储服务_

## 在S3上新建存储桶

- 新建一个存储桶作为数据推上来存放的位置，比如说`databackup`,那么完整的S3路径就是`s3://databackup`。

- 如果是备份到特定文件夹`data`,那么路径就是`s3://databackup/data`。

## 本地安装python3 和 命令行工具AWS CLI

- 安装[python3](https://www.python.org/downloads/windows/)

- 安装windows版本的[aws cli](https://docs.amazonaws.cn/cli/latest/userguide/install-windows.html)

- 打开windwos的cmd验证下：

```
C:\Users\god>aws --version
aws-cli/2.0.7 Python/3.7.5 Windows/10 botocore/2.0.0dev11
```

- 配好AKSK， AKSK的key是在创建aws用户的时候让你下载的一个csv文件，记得妥善保管。

```
$ aws configure
AWS Access Key ID [****************xxxx]:	# 输入你的AK key
AWS Secret Access Key [****************xxxx]: # 输入你的SK key
Default region name [cn-northwest-1]:  # 宁夏：cn-northwest-1，北京：cn-north-1
Default output format [json]: 	# 默认json

# 配好以后应该是这样的

C:\Users\god>aws configure list
      Name                    Value             Type    Location
      ----                    -----             ----    --------
   profile                <not set>             None    None
access_key     ****************P3UC shared-credentials-file
secret_key     ****************rV4p shared-credentials-file
    region           cn-northwest-1      config-file    ~/.aws/config
```

- 测试key是否配成功：

```
C:\Users\god>aws s3 ls
2019-09-07 16:19:46 god
2020-01-29 19:10:27 lovevideo
2020-08-09 12:49:07 publicuse
```

## 启用windows的定时任务

- 依次打开 控制面板 - 管理工具 - 任务计划程序 - 点击 **创建任务**

![task][1]

- **常规栏** 的名称写为`s3sync`, **触发器栏** 新建一个定时任务，设定好时间和频率。

![trigger][2]

- **操作栏** 新建一个操作。

[OPTION1] 如果每次都通盘同步，程序和脚本选择本机装的aws cli程序所在的位置，参数就写对应的同步参数。

程序或脚本： C:\Program Files\Amazon\AWSCLIV2\aws.exe

添加参数： s3 sync Z:\data s3://databackup/data --storage-class GLACIER

[OPTION2] 如果只想同步特定文件夹，可以自己写个python 脚本指定，那么程序和脚本选择本机装的python.exe程序所在的位置，参数就写对应的python脚本。

程序或脚本： C:\Users\god\AppData\Local\Programs\Python\Python38\python.exe

添加参数： Z:\scripts\s3sync.py


参考脚本s3sync.py如下：

```py
#!/usr/bin/python

# 本脚本会自动检测特定目录下的最新文件夹，自动备份到aws s3的归档
# 第一步，先在当前操作系统安装python https://www.python.org/downloads/release/python-382/
# 第二步，修改以下路径，并运行本程序

import os

test_report = "Z:\\"   #需要修改！需要同步的最新文件夹所在的上级文件夹路径
s3dir = r"s3://databackup/data" #修改！ s3同步路径

def new_report(test_report): # 找到最新文件夹的路径和名称
    lists = os.listdir(test_report)  #列出目录的下所有文件和文件夹保存到lists
    print(list)
    lists.sort(key=lambda fn:os.path.getmtime(test_report + "\\" + fn)) #按时间排序
    file_new = os.path.join(test_report,lists[-1])
    filename = lists[-1] #获取最新的文件保存到file_new
    print(file_new)
    return file_new,filename


latest=new_report(test_report) # 找出当前文件夹下的最新文件夹路径和名字
print (latest)
os.system("aws s3 sync  %s %s/%s --storage-class GLACIER" % (latest[0],s3dir,latest[1])) # 执行同步命令
```


**TIPS** 如果每次同步多个文件夹，AWS CLI是支持运行多个sync命令的，只需要在你的脚本里运行多条同步任务即可,但任务太多会影响本机的性能哦。

```
aws s3 sync Z:/data1 s3://databackup/data1            

aws s3 sync Z:/data2 s3://databackup/data2
```


- 点击确定，保存计划任务，就可以中间的任务清单里看到这条命叫`s3sync`的定时任务了。

- 选中这条任务，点击右侧操作列表里的运行按钮进行测试, 同步完成以后就可以在AWS控制台里看到上传且已经归档的文件了。

![test1][3]

![test2][4]


## 确认下数据自动执行

- 等到下个备份周期check一下上次备份有没有自动完成，云端有没有数据就正常使用了。

[S3 相关命令行文档](https://docs.amazonaws.cn/cli/latest/userguide/cli-services-s3-commands.html)
[S3 sync](https://docs.aws.amazon.com/cli/latest/reference/s3/sync.html)
[如何提高 Amazon S3 的同步命令传输性能](https://aws.amazon.com/cn/premiumsupport/knowledge-center/s3-improve-transfer-sync-command/)



> 人们愤怒地指责那个罪犯，举起手里的石头就要砸，耶稣说：自认为无罪的人都可以砸。所有人都放下了手中的石头。