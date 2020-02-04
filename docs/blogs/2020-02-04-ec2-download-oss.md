# 直接从ec2下载阿里云oss数据

> 国内不少测序公司都提供阿里云的oss下载链接来交付数据，我们会下载到本地进行分析，但是如果我用了aws，是不是还要从本地上传到aws上，那多麻烦。其实呢，我们可以直接从ec2去拉阿里的数据就好了，而且速度杠杠的！当然这不限于下载外包数据，如果需要云间数据迁移，也是极好的，而且貌似ali对流量带宽是有限制的，而aws就比较实在都给你都给你。
>
> -- D.C

_名词解释：aws的s3 对应 阿里的oss，ec2 对应 阿里的ecs_

## 安装ossutil64到ec2

接触过阿里云的都知道，ossutil64命令是以命令行方式管理OSS数据的工具。要下载阿里的数据，我们就得先安装这个命令。

- 创建/登录一台ec2，只要不是t系列就行，因为t系列的带宽有限制。比如我登录的是一台`m5.large`。接着`wget`下载命令，`chmod`修改权限。(创建ec2前先知道待下载数据有多大，来设定我的EBS盘大小)

```bash
$ wget http://gosspublic.alicdn.com/ossutil/1.6.10/ossutil64
--2020-02-04 15:05:54--  http://gosspublic.alicdn.com/ossutil/1.6.10/ossutil64
Resolving gosspublic.alicdn.com (gosspublic.alicdn.com)... 221.236.10.175, 117.34.40.113, 118.112.19.115, ...
Connecting to gosspublic.alicdn.com (gosspublic.alicdn.com)|221.236.10.175|:80... connected.
HTTP request sent, awaiting response... 200 OK
Length: 10118253 (9.6M) [application/octet-stream]
Saving to: 'ossutil64'

100%[====================================================================================================================>] 10,118,253  12.0MB/s   in 0.8s

2020-02-04 15:05:55 (12.0 MB/s) - 'ossutil64' saved [10118253/10118253]

$ chmod 755 ossutil64

$ ./ossutil64 -v
ossutil version: v1.6.10
```

## 运行ossutil64下载

- 用以下命令下载oss数据到ec2当前路径。运行`./ossutil64 help cp` 查看更多说明。

```bash
./ossutil64 cp oss://bucketname/myfolder ./ -r -i <AccessKeyID> -k <AccessKeySecret> -e <endpoint>
```

有四个信息需要问您的服务商拿到：

1. 数据在oss上的完整路径
2. `<AccessKeyID>` 对应 `-i`
3. `<AccessKeySecret>` 对应 `-k`
4. oss的endpoint 对应 `-e`


举例：

```bash
$ ./ossutil64 cp oss://delivery-data/888/Project_s88_20Samples_20191104_123456 ./ -r -i ABCDEFG123456 -k 1a2b3c4d5e6fABCDE -e http://oss-cn-shanghai.aliyuncs.com
```


> 你只有一次机会来完成这件事。


_附：阿里云oss的Region和Endpoint对照表_

|Region中文名称|Region英文表示|外网Endpoint|传输加速Endpoint|ECS访问的内网Endpoint|支持HTTPS|
|-------------|-------------|-------------|-------------|-------------|-------------|
|华东 1（杭州）|oss-cn-hangzhou|oss-cn-hangzhou.aliyuncs.com|oss-accelerate.aliyuncs.com|oss-cn-hangzhou-internal.aliyuncs.com|是|
|华东 2（上海）|oss-cn-shanghai|oss-cn-shanghai.aliyuncs.com|oss-accelerate.aliyuncs.com|oss-cn-shanghai-internal.aliyuncs.com|是|
|华北 1（青岛）|oss-cn-qingdao|oss-cn-qingdao.aliyuncs.com|oss-accelerate.aliyuncs.com|oss-cn-qingdao-internal.aliyuncs.com|是|
|华北 2（北京）|oss-cn-beijing|oss-cn-beijing.aliyuncs.com|oss-accelerate.aliyuncs.com|oss-cn-beijing-internal.aliyuncs.com|是|
|华北 3（张家口）|oss-cn-zhangjiakou|oss-cn-zhangjiakou.aliyuncs.com|oss-accelerate.aliyuncs.com|oss-cn-zhangjiakou-internal.aliyuncs.com|是|
|华北 5（呼和浩特）|oss-cn-huhehaote|oss-cn-huhehaote.aliyuncs.com|oss-accelerate.aliyuncs.com|oss-cn-huhehaote-internal.aliyuncs.com|是|
|华南 1（深圳）|oss-cn-shenzhen|oss-cn-shenzhen.aliyuncs.com|oss-accelerate.aliyuncs.com|oss-cn-shenzhen-internal.aliyuncs.com|是|
|华南 2（河源）|oss-cn-heyuan|oss-cn-heyuan.aliyuncs.com|无|oss-cn-heyuan-internal.aliyuncs.com|是|
|西南 1（成都）|oss-cn-chengdu|oss-cn-chengdu.aliyuncs.com|oss-accelerate.aliyuncs.com|oss-cn-chengdu-internal.aliyuncs.com|是|
|中国（香港）|oss-cn-hongkong|oss-cn-hongkong.aliyuncs.com|oss-accelerate.aliyuncs.com|oss-cn-hongkong-internal.aliyuncs.com|是|
|美国西部 1 （硅谷）|oss-us-west-1|oss-us-west-1.aliyuncs.com|oss-accelerate.aliyuncs.com|oss-us-west-1-internal.aliyuncs.com|是|
|美国东部 1 （弗吉尼亚）|oss-us-east-1|oss-us-east-1.aliyuncs.com|oss-accelerate.aliyuncs.com|oss-us-east-1-internal.aliyuncs.com|是|
|亚太东南 1 （新加坡）|oss-ap-southeast-1|oss-ap-southeast-1.aliyuncs.com|oss-accelerate.aliyuncs.com|oss-ap-southeast-1-internal.aliyuncs.com|是|
|亚太东南 2 （悉尼）|oss-ap-southeast-2|oss-ap-southeast-2.aliyuncs.com|oss-accelerate.aliyuncs.com|oss-ap-southeast-2-internal.aliyuncs.com|是|
|亚太东南 3 （吉隆坡）|oss-ap-southeast-3|oss-ap-southeast-3.aliyuncs.com|oss-accelerate.aliyuncs.com|oss-ap-southeast-3-internal.aliyuncs.com|是|
|亚太东南 5 （雅加达）|oss-ap-southeast-5|oss-ap-southeast-5.aliyuncs.com|oss-accelerate.aliyuncs.com|oss-ap-southeast-5-internal.aliyuncs.com|是|
|亚太东北 1 （日本）|oss-ap-northeast-1|oss-ap-northeast-1.aliyuncs.com|oss-accelerate.aliyuncs.com|oss-ap-northeast-1-internal.aliyuncs.com|是|
亚太南部 1 （孟买）|oss-ap-south-1|oss-ap-south-1.aliyuncs.com|无|oss-ap-south-1-internal.aliyuncs.com|是|
|欧洲中部 1 （法兰克福）|oss-eu-central-1|oss-eu-central-1.aliyuncs.com|oss-accelerate.aliyuncs.com|oss-eu-central-1-internal.aliyuncs.com|是|
|英国（伦敦）|oss-eu-west-1|oss-eu-west-1.aliyuncs.com|oss-accelerate.aliyuncs.com|oss-eu-west-1-internal.aliyuncs.com|是|
|中东东部 1 （迪拜）|oss-me-east-1|oss-me-east-1.aliyuncs.com|无|oss-me-east-1-internal.aliyuncs.com|是|
