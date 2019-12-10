# aws
*aws tools for daily easy use*
***

## 1. pcluster build guide on aws

### launch an instance to install pcluster
- c5.large
- remember your keypair name `eg. mykey.pem`
- launch & login

### be root
- `sudo su -`
- `wget https://github.com/DavisChen99/aws/archive/master.zip`
- `unzip master.zip && cd aws-master`
- `cat README.md`
- add permission `chmod 667 install_pcluster_v1.sh`
- run `bash install_pcluster_v1.sh`

### build manually (after first build)
- `vim config` as you want
- `aws configure` with your AKSK keys
- `pcluster <create/delete> <cluster_template>`

### check service
- go to aws console & check your nodes
- log in master ndoes to check:
  * `qhost` to check your queue
  * `df -h` to check your volumns
  * `qsub test.sh` to check your cluster function
  * `qstat -f` to see job status

*by Davis 20191210*
