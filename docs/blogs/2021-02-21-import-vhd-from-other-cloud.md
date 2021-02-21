# 高阶15 - 如何导入其他云商的虚拟机镜像

> 天下大势，分久必分，分久必合。同样云计算市场分分合合，来来去去也正常，有不少朋友以前用的是非AWS的云，
> 但是要么就是踩坑了要么就是开始割韭菜了，想要迁移到AWS上，在这过程中可能遇到最多的问题是服务器镜像的迁移，
> 本文就抛砖引玉，利用VM Import服务来导入镜像，生成能在AWS上使用的AMI镜像。
> -- D.C

VM Import/Export 支持的映像类型很多，比如：OVA，VHD／VHDX，VMDK，RAW。

### 映像格式

VM Import/Export 支持以下映像格式来导入磁盘和 VMs：

- 启动虚拟装置 (OVA) 映像格式，该格式支持将映像与多个硬盘一起导入。

- 流优化型 ESX 虚拟机磁盘 （VMDK） 映像格式，该格式与 VMware ESX 和 VMware vSphere 虚拟化产品兼容。

- 固定和动态虚拟硬盘 (VHD/VHDX) 映像格式，该格式与 Microsoft Hyper-V、Microsoft Azure 和 Citrix Xen 虚拟化产品兼容。

- 用于导入磁盘和 VMs 的原始格式。

更多条件请查询 [点我](https://docs.aws.amazon.com/zh_cn/vm-import/latest/userguide/vmie_prereqs.html)


### 准备工作

- 首先，需要在非AWS的云端，将我们要迁移的服务器打成一个标准镜像，一般都是vhd格式的，比如名字叫 `abcd`。


- 将这个镜像文件想办法导到AWS账号下的S3桶里，比如放在名字叫 `tempimage`  的桶里,那么这个文件的s3路径就是:

```
s3://tempimage/abcd
```

镜像导到S3可以有2种方式：

1. 利用同步工具，直接从某云的对象存储拉到AWS的S3。
2. 以文件的形式下载到本地，再上传到AWS S3。

- 在本机电脑上安装AWS CLI，并配置好 AKSK。具体方法可以参考 [入门帖](https://www.bioaws.com/blogs/2020-02-01-s3-data-cli/)


### 权限设置


总而言之，就是让用户拥有操作S3，EC2相关动作的权限。


- 进入AWS console界面的IAM，点击左侧的 **策略**，点击 **创建策略**，选择添加json格式策略，输入如下策略并保存,命名为 `vmimport_policy`。

```json
{

    "Version": "2012-10-17",

    "Statement": [

        {

            "Effect": "Allow",

            "Action": [

                "s3:GetBucketLocation",

                "s3:GetObject",

                "s3:ListBucket"

            ],

            "Resource": [

                "arn:aws-cn:s3:::tempimage",

                "arn:aws-cn:s3:::tempimage/*"

            ]

        },

        {

            "Effect": "Allow",

            "Action": [

                "ec2:ModifySnapshotAttribute",

                "ec2:CopySnapshot",

                "ec2:RegisterImage",

                "ec2:Describe*"

            ],

            "Resource": "*"

        }

    ]

}

```

![policy][1]

- 进入AWS console界面的IAM，点击左侧的角色，新建一个角色命名为 `vmimport`, 在询问策略的时候选中我们刚刚创建的策略 `vmimport_policy`, 创建角色。

![choosepolicy][2]

- 再回到 `vmimport` 这个角色界面，点击 **信任关系** ，然后点击 **编辑信任关系**，输入如下策略，后点击 **更新信任策略**。 可以看到显示为 `身份提供商 vmie.amazonaws.com`。

```json
{

  "Version": "2012-10-17",

  "Statement": [

    {

      "Effect": "Allow",

      "Principal": {

        "Service": "vmie.amazonaws.com"

      },

      "Action": "sts:AssumeRole",

      "Condition": {

        "StringEquals": {

          "sts:Externalid": "vmimport"

        }

      }

    }

  ]

}
```

![addtrust][3]

### 运行命令转化镜像

- 本地终端，新建一个json文件如下,命名为 `containers.json `

```json
[
  {
    "Description": "My Server1",
    "Format": "VHD",
    "UserBucket": {
        "S3Bucket": "tempimage",
        "S3Key": "abcd1"
    }
}]
```

- 本地终端运行AWS CLI 命令,进行镜像转化，结果会返回一个作业id 如 `import-ami-1234567890abcdef0` 。

```
$ aws ec2 import-image --description "My server VM" --disk-containers "file://D:\containers.json"
```

- 查看转化状态。

```
aws ec2 describe-import-image-tasks --import-task-ids import-ami-1234567890abcdef0
```

Status的状态值有如下几种：

active — The import task is in progress.

deleting — The import task is being canceled.

deleted — The import task is canceled.

updating — Import status is updating.

validating — The imported image is being validated.

validated — The imported image was validated.

converting — The imported image is being converted into an AMI.

completed — The import task is completed and the AMI is ready to use.


- 转化完毕，就可以在EC2界面左侧的AMI 列表中找到对应的镜像，再通过这个镜像启动EC2即可。

### 如果转化磁盘镜像(snapshot)

- 假设导出的磁盘镜像名字为 `abcd_disk`, 同样存放在S3的 `tempimage`桶里，那么只要在本地终端运行如下命令, 结果会返回一个作业id 如 `import-snap-1234567890abcdef0` 。

```
$ aws ec2 import-snapshot --description "My server VM" --disk-container "file://C:\containers.json"
```

containers.json 的格式如下：

```
{
    "Description": "My server disk",
    "UserBucket": {
        "S3Bucket": "tempimage",
        "S3Key": "abcd_disk"
    }
}
```

- 根据作业id查看snapshot转化状态。

```
$ aws ec2 describe-import-snapshot-tasks --import-task-ids import-snap-1234567890abcdef0
```

![snapshotstatus][5]

- 转化完成后，就可以在ec2界面的左侧EBS下的快照里找到转化后的磁盘，再将它attach到需要的ec2上即可。


## 补充材料：

- [VM Import/Export](https://docs.aws.amazon.com/zh_cn/vm-import/latest/userguide/what-is-vmimport.html)



> 我只是一个句号。
