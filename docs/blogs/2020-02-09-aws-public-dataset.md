# 福音！用好AWS公开数据集

>aws 提供了一个s3存储空间，给那些开放公共下载的资源，并且存储费用是免费的！比如我们生信常用的NCBI SRA，ENCODE, 1000g，NIH的人类微生物组计划数据，nanopore reference, 水稻基因组3000 Rice Genomics, TCGA,ICGC数据等，有了这些有什么好处呢？没错，如果我是一名aws用户，我就需要再去下载数据啦，大家都知道网速那个慢呐~ 我只需要知道数据所在的aws的位置，通过aws内网把想要的数据直接拉到我要做分析的机器上就可以，速度飞起！
>
>--- D.C

[AWS public dataset](https://registry.opendata.aws/)

## 什么是公开数据集

场景：在做数据分析时，一个困难是海量的数据本地存储困难，而且下载耗费的时间极长。例如1T数据，如果下载网速是3MBps（目前中国的平均宽带速度），那要4天才能下载完。有些数据集有几十T，那光下载就要几个月。

AWS云服务平台上为了解决这个困难提供了很多常用的大规模数据集 Public Data Sets https://aws.amazon.com/datasets ，无需下载即可在亚马逊AWS EC2上使用。

目的是：

- 通过提供公开数据用于AWS分析，实现数据访问的民主化。

- 开发新的基于云的技术、格式和工具，降低使用数据的成本。

- 鼓励并发展从共享数据集中受益的用户社区。

![dataset_list][1]

挑其中两个数据介绍下：

- TCGA（癌症基因组地图集）语料库囊括了从数以千计的癌症患者处收集来的原始和加工过的基因组，转录基因组，和表观基因组数据，现在在 AWS S3 上对 [Cancer Genomics Cloud（CGC）](http://iphone.myzaker.com/zaker/link.php?pk=56618d7c1bc8e0fb12000008&b=aHR0cDovL3d3dy5jYW5jZXJnZW5vbWljc2Nsb3VkLm9yZy8=&bcode=9fe315b9&target=_new)的用户免费开放。 [Cancer Genomics Cloud](http://iphone.myzaker.com/zaker/link.php?pk=56618d7c1bc8e0fb12000008&b=aHR0cDovL2NhbmNlcmdlbm9tZS5uaWguZ292L2Fib3V0dGNnYQ==&bcode=fde6976f&target=_new)是一个试点云项目，由美国国家癌症研究所资助，在 [Seven Bridges Genomics](http://iphone.myzaker.com/zaker/link.php?pk=56618d7c1bc8e0fb12000008&b=aHR0cHM6Ly93d3cuc2JnZW5vbWljcy5jb20v&bcode=f10ef67a&target=_new)平台上运行。

- ICGC（国际肿瘤基因组协作组）泛癌症数据集因 PCAWG（全基因组泛癌症分析）研究产生，现在在 AWS 上也可用，使癌症研究者可以访问 2400 多组被持续分析的基因组，这些基因组对应于 1100 多位独特的 ICGC 捐赠者。这些数据也将在 AWS S3 上对那些符合 ICGC 数据共享策略，受到信任的研究者免费开放。

## 如何使用数据集

- [AWS public dataset](https://registry.opendata.aws/) 打开后，选中我要使用的数据集，点击进入，可以看到关于这个数据集的完整**描述**，**授权**，**文档**，**联系方式**，以及**使用案例**，右侧还有这个数据资源在aws的资源名称（**ARN**） `arn:aws:s3:::1000genomes`，和所在的区域 `us-east-1`。 一般呢我会点击文档进去看一眼它的readme，确认没错过什么需要注意的地方，然后登录到我的EC2，根据ARN我知道，这个数据放在s3的一个名为 _1000genomes_ 的桶里，用aws cli命令进去看看吧。

![dataset_1000g][2]

```bash
$ aws s3 ls s3://1000genomes
                           PRE 1000G_2504_high_coverage/
                           PRE alignment_indices/
                           PRE changelog_details/
                           PRE complete_genomics_indices/
                           PRE data/
                           PRE hgsv_sv_discovery/
                           PRE phase1/
                           PRE phase3/
                           PRE pilot_data/
                           PRE release/
                           PRE sequence_indices/
                           PRE technical/
2015-09-08 21:16:09       1663 20131219.populations.tsv
2015-09-08 21:17:01         97 20131219.superpopulations.tsv
2015-09-08 15:01:44     257098 CHANGELOG
2014-09-02 15:39:53      15977 README.alignment_data
2014-01-30 11:13:29       5289 README.analysis_history
2014-01-31 03:44:08       5967 README.complete_genomics_data
2014-08-29 00:22:38        563 README.crams
2013-08-06 16:11:58        935 README.ebi_aspera_info
2013-08-06 16:11:58       8408 README.ftp_structure
2014-09-02 21:19:43       2082 README.pilot_data
2014-09-03 12:33:15       1938 README.populations
2013-08-06 16:11:58       7857 README.sequence_data
2015-06-18 18:28:31        672 README_missing_files_20150612
2015-06-03 19:43:32        136 README_phase3_alignments_sequence_20150526
2015-06-18 16:34:45        273 README_phase3_data_move_20150612
2014-09-03 12:34:30    3579471 alignment.index
2014-09-03 12:32:59   54743580 analysis.sequence.index
2014-09-03 12:34:57    3549051 exome.alignment.index
2014-09-03 12:35:15   67069489 sequence.index

```

- 找到我想要的数据，直接用命令`aws sync s3://1000genomes/path/to/data ~/ref/1000g/` 拉到自己机器上分析就OK，是不是很方便呢？

```bash 
$ aws s3 sync s3://1000genomes/1000G_2504_high_coverage ./
Completed 320.2 MiB/~76.9 GiB (152.0 MiB/s) with ~5 file(s) remaining (calculating...)
```

- 如果我还是不会用，没关系，看看**使用说明**，里面包括很多教程和工具集。

[Usage examples for all datasets](https://registry.opendata.aws/tag/life-sciences/usage-examples/)



## 如何公布我的数据集

- 如果我手里有训练好的模型，有自己整理的很好用的数据库，或者是任何我觉得别人用得上的，能改变人类命运的等等数据，我都可以申请将我的数据集放到aws的这个公开数据集平台上，这样一来，全世界的用户都能看到，用到我公开的数据集，去不断的传播，丰富，完善这个数据集，集全球智慧将一个事情做到极致，这就是开源的终极奥义。
- 当然，既然是免费的，aws自然也有自己的一套审核标准，要通过AWS公共数据集程序共享数据集，就必须同意AWS公共数据集程序的条款和条件，这些条款和条件可从[这个网址](https://AWS.amazon.com/Public-datasets/Terms/)获得。
- 申请人需要填写一些表格提交[申请](https://application.opendata.aws/)，等待审核以通过以后，就可以上传数据了。
- 当然最靠谱的是找到aws的人，让他来给指导我怎么申请，这样最高效。

![dataset_apply][3]

## 需要注意的

- aws公开数据集分国内和国外，记得看清楚，可不要命令敲了半天才发现是国内的机器在访问国外的数据集。
- 公开数据集是免费的，网站上很多数据都是直接就能下载的。但是如果我是数据提供方，我想对分享实现一些控制，比如说别人想用我的数据需要我授权，当然，还是免费使用，也是可以的。
- aws 每3个月对数据集的申请进行一次评估，每个季度的截至日期是3.31，6.30，9.30，12.31，或者是这天的下一个工作日。如果想上传自己的数据集的话，建议提前准备。
- 公开数据集的免费，包括数据存储费和数据传输费，所以不需要支付任何费用。



>王权没有永恒。



### 一些有意思的数据集



- [1980 US Census](https://aws.amazon.com/datasets/2310) 美国1980年人口普查数据

Data from the 1980 US Census

 

- [1990 US Census](https://aws.amazon.com/datasets/2304) 美国1990年人口普查数据

Data from the 1990 US Census

 

- [2000 US Census](https://aws.amazon.com/datasets/2290) 美国2000年人口普查数据

Data from the 2000 US Census

 

- [2003-2006 US Economic Data](https://aws.amazon.com/datasets/2341) 美国2003-2006经济数据

US Economic Data for years 2003 to 2006

 

- [2008 TIGER/Line Shapefiles](https://aws.amazon.com/datasets/2367) 美国2000年人口普查与详细的政区划分

Census 2000 and Current United States shapefiles

 

- [3D Version of the PubChem Library](https://aws.amazon.com/datasets/2284) PubSem有机小分子生物活性数据三维版

3D Version of the PubChem Library

 

- [AnthroKids – Anthropometric Data of Children](https://aws.amazon.com/datasets/2351) 70年代的儿童人体测量数据

Anthropometric data on children from two studies in 1975 and 1977

 

- [Apache Software Foundation Public Mail Archives](https://aws.amazon.com/datasets/7791434387204566) Apache基金会的到2011年为止的邮件列表

A collection of all publicly available Apache Software Foundation mail archives as of July 11, 2011

 

- [Business and Industry Summary Data](https://aws.amazon.com/datasets/2342) 美国工商业数据

US Business and Industry Summary Data

 

- [C57BL/6J by C3H/HeJ Mouse Cross (Sage Bionetworks)](https://aws.amazon.com/datasets/4170) 老鼠杂交数据

C57BL/6J by C3H/HeJ mouse cross from the Jake Lusis lab at UCLA

 

- [Common Crawl Corpus](https://aws.amazon.com/datasets/41740) 50亿网页

A corpus of web crawl data composed of over 5 billion web pages. This data set is freely available on Amazon S3 and is released under the Common Crawl Terms of Use.

 

- [Daily Global Weather Measurements, 1929-2009 (NCDC, GSOD)](https://aws.amazon.com/datasets/2759) 80年的按日全球天气数据

A collection of daily weather measurements (temperature, wind speed, humidity, pressure, &c.) from 9000+ weather stations around the world.

 

- [DBpedia 3.5.1](https://aws.amazon.com/datasets/2319) DBpedia结构化知识库

DBpedia is a community effort to extract structured information from Wikipedia and to make this information available on the Web

 

- [Denisova Genome](https://aws.amazon.com/datasets/2357) 丹尼索瓦人基因组

The high-coverage genome sequence of a Denisovan individual sequenced to ~30x coverage on the Illumina platform. Together with their sister group the Neandertals, Denisovans are the most closely related extinct relatives of currently living humans.

 

- [Enron Email Data](https://aws.amazon.com/datasets/917205) 安然电子邮件数据

Enron email data publicly released as part of FERC’s Western Energy Markets investigation converted to industry standard formats by EDRM. The data set consists of 1,227,255 emails with 493,384 attachments covering 151 custodians. The email is provided in Microsoft PST, IETF MIME, and EDRM XML formats.

 

- [Ensembl – FASTA Database Files](https://aws.amazon.com/datasets/2594) Ensembl真核生物基因组转录与翻译模型

Ensembl sequence databases of transcript and translation models

 

- [Ensembl Annotated Human Genome Data (FASTA Release 73)](https://aws.amazon.com/datasets/3841) 人类与其他50个物种的基因序列

The Ensembl project produces genome databases for human as well as over 50 other species, and makes this information freely available.

 

- [Ensembl Annotated Human Genome Data (MySQL Release 73)](https://aws.amazon.com/datasets/2315) 人类与其他50个物种的基因序列，MySQL版

The Ensembl project produces genome databases for human as well as over 50 other species, and makes this information freely available.

 

- [Federal Contracts from the Federal Procurement Data Center (USASpending.gov)](https://aws.amazon.com/datasets/2406) 美国联邦政府的合同

A data dump of all federal contracts from the Federal Procurement Data Center found at USASpending.gov.

 

- [Federal Reserve Economic Data – Fred](https://aws.amazon.com/datasets/2443) 美联储经济数据时间序列

Database of 20,059 U.S. economic time series.

 

- [Freebase Data Dump](https://aws.amazon.com/datasets/2320) Freebase知识图谱

Freebase is an open database of the world’s information, covering millions of topics in hundreds of categories

 

- [Freebase Quad Dump](https://aws.amazon.com/datasets/2052645406658757) Freebase知识图谱四元组格式

A data dump of all the current facts and assertions in Freebase

 

- [Freebase Simple Topic Dump](https://aws.amazon.com/datasets/8247878934976180) Freebase知识图谱简化的主题数据

A data dump of the basic identifying facts about every topic in Freebase

 

- [GenBank](https://aws.amazon.com/datasets/2261) 基因银行序列数据库

An annotated collection of all publicly available DNA sequences including more than 85.7B bases and 82.8M sequence records.

 

- [Google Books Ngrams](https://aws.amazon.com/datasets/8172056142375670) 谷歌图书的ngram语言模型

A data set containing Google Books n-gram corpuses. This data set is freely available on Amazon S3 in a Hadoop friendly file format and is licensed under a Creative Commons Attribution 3.0 Unported License. The original dataset is available from http://books.google.com/ngrams/.

 

- [Human Liver Cohort (Sage Bionetworks)](https://aws.amazon.com/datasets/4181) 人类肝脏基因表达

Human Liver Cohort characterizing gene expression in liver samples

 

- [Human Microbiome Project](https://aws.amazon.com/datasets/1903160021374413) 人体微生物群数据

Human Microbiome Project Data Set

 

- [Illumina – Jay Flatley (CEO of Illumina) Human Genome Data Set](https://aws.amazon.com/datasets/3357) 人体基因组数据

Jay Flatley (CEO of Illumina) human genome data set.

 

- [Influenza Virus (including updated Swine Flu sequences)](https://aws.amazon.com/datasets/2419) 流感病毒数据

NCBI Influenza Resource Center Data.

 

- [Japan Census Data](https://aws.amazon.com/datasets/2285) 日本人口统计数据

Multiple data sets including: (1) Population Census of Japan (1995, 2000, 2005, 2010), (2) Establishment and Enterprise Census of Japan (1999, 2001, 2004, 2006), and (3) Economic Census of Japan (2009).

 

- [Labor Statistics Databases](https://aws.amazon.com/datasets/2287) 美国劳工部的统计数据

Various Labor Statistics

 

- [M-Lab dataset: Network Diagnostic Tool (NDT)](https://aws.amazon.com/datasets/3190) 2009年互联网性能（如网速）诊断数据

NDT test results created through Measurement Lab (M-Lab) between February 2009 and September 2009

 

- [M-Lab dataset: Network Path and Application Diagnosis tool (NPAD)](https://aws.amazon.com/datasets/3189) 2009年互联网路由，包头等测试数据

NPAD test results created through Measurement Lab (M-Lab) between February 2009 and September 2009

 

- [Marvel Universe Social Graph](https://aws.amazon.com/datasets/5621954952932508) 一个虚拟的社交网络关系图

This dataset is an example of a social collaboration network based on the characters in The Marvel Universe, that is, the artificial world that takes place in the universe of the Marvel comic books.

 

- [Material Safety Data Sheets](https://aws.amazon.com/datasets/6247470578246837) 材料安全数据

230,000 Material Safety Data Sheets.

 

- [Million Song Dataset](https://aws.amazon.com/datasets/6468931156960467) 百万歌曲数据

The Million Songs Collection is a collection of 28 datasets containing audio features and metadata for a million contemporary popular music tracks.

 

- [Million Song Sample Dataset](https://aws.amazon.com/datasets/1330518334244589) 百万歌曲数据库的1万子集

This is a 10,000 song subset of audio features and metadata from the Million Songs collection – a collection of 28 datasets containing audio features and metadata for a million contemporary popular music tracks.

 

- [Model Organism Encyclopedia of DNA Elements (modENCODE)](https://aws.amazon.com/datasets/8042906995278110)  模式生物生命百科全书

A collection of data from the modENCODE project ( [http://www.modencode.org ](http://www.modencode.org/))

 

- [NASA NEX](https://aws.amazon.com/datasets/1571164061367186) NASA的地球卫星地图与气候变迁

Three NASA NEX datasets are now available, including climate projections and satellite images of Earth.

 

- [OpenStreetMap Rendering Database](https://aws.amazon.com/datasets/2844) 开源的全球地图数据

A PostGIS 8.3 data cluster of all OpenStreetMap data for the planet.

 

- [Petroleum Public Data Set (working Title)](https://aws.amazon.com/datasets/2900) 石油数据

Public-domain data for the oil & gas industry, assembled from the contributions of participating agencies in the United States, Canada and around the world. This data provides industry stakeholders with an opportunity to focus their efforts on the analysis and interpretation of this data without concern for the trivial and time-consuming tasks of locating, downloading, reformatting and integrating the data prior to value-added work being performed.

 

- [PubChem Library](https://aws.amazon.com/datasets/2286) 有机小分子生物活性数据

A data set of information on the biological activities of small molecules.

 

- [Sloan Digital Sky Survey DR6 Subset](https://aws.amazon.com/datasets/2797) 斯隆数字化巡天

The Sloan Digital Sky Survey is the most ambitious astronomical survey ever undertaken.

 

- [The Cannabis Sativa Genome](https://aws.amazon.com/datasets/3448202235644016) 大麻基因

Whole Genome Shotgun Sequencing of the Cannabis Sativa Cultivar “Chemdawg”

 

- [The WestburyLab USENET corpus](https://aws.amazon.com/datasets/1679761938200766) 4万多个USENET新闻组数据

The WestburyLab USENET corpus is an anonymized compilation of postings from 47,860 English-language newsgroups from 2005-2010.

 

- [Transportation Databases](https://aws.amazon.com/datasets/2289) 美国交通部的航空，航海，公路，铁路，管道，自行车等统计数据

Various transportation statistics

 

- [Twilio/Wigle.net Street Vector Data Set](https://aws.amazon.com/datasets/2408) 完整的美国街道名与地址

Twilio/Wigle.net database of mapped US street names and address ranges.

 

- [Unigene](https://aws.amazon.com/datasets/2283) NCBI的转录组数据库

UniGene: An Organized View of the Transcriptome.

 

- [University of Florida Sparse Matrix Collection](https://aws.amazon.com/datasets/2379) 佛罗里达大学的稀疏矩阵数据集

The University of Florida Sparse Matrix Collection is a large, widely available, and actively growing set of sparse matrices that arise in real applications.

 

- [Wikipedia Extraction (WEX)](https://aws.amazon.com/datasets/2345) 维基百科用Freebase增强过的结构化数据

A processed dump of the English language Wikipedia

 

- [Wikipedia Page Traffic Statistic V3](https://aws.amazon.com/datasets/6025882142118545) 维基百科2011年3个月的按小时访问量

This dataset contains a 150 GB sample of the data used to power [trendingtopics.org](http://www.trendingtopics.org/). It includes a full 3 months of hourly page traffic statistics from Wikipedia (1/1/2011-3/31/2011).

 

- [Wikipedia Page Traffic Statistics](https://aws.amazon.com/datasets/2596) 维基百科2009年7个月的按小时访问量

Contains 7 months of hourly pageview statistics for all articles in Wikipedia

 

- [Wikipedia Traffic Statistics V2](https://aws.amazon.com/datasets/4182) 维基百科2009-2010年16个月按小时访问量

Contains 16 months of hourly pageview statistics for all articles in Wikipedia

 

- [Wikipedia XML Data](https://aws.amazon.com/datasets/2506) 维基百科2009版，XML格式

A complete copy of all Wikimedia wikis, in the form of wikitext source and metadata embedded in XML.

 

- [YRI Trio Dataset](https://aws.amazon.com/datasets/2899) 三个约鲁巴人的完整基因组

Complete genome sequence data for three Yoruba individuals from Ibadan, Nigeria



