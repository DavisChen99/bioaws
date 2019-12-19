# aws
*aws tools for daily easy use*
***

## pcluster quick-build

### launch an instance to install pcluster (v2.5.1)
- `eg. t2.micro`
- remember your keypair name `eg. mykey.pem`
- launch & login

### be root
- `sudo su -`
- `wget https://github.com/DavisChen99/aws/archive/master.zip`
- `unzip master.zip && cd aws-master`
- `cat README.md` & refer to https://aws-parallelcluster.readthedocs.io/en/latest/configuration.html#scheduler
- add permission `chmod 667 install_pcluster_v1.sh`
- run `bash install_pcluster_v1.sh`, try again if you meet HTTPS connect problem - usually network issue.

### build manually (after first build)
- `vim config` as you want
- `aws configure` with your AKSK keys
- `pcluster <create/delete> <cluster_template>`

### check service
- go to aws console & check your nodes
- log in master nodes to check:
  * `qhost` to check your queue
  * `df -h` to check your volumns
  * `qsub test.sh` to check your cluster function
  * `qstat -f` to see job status
- submit your jobs using command like `qsub -cwd -S /bin/bash -V -l vf=2G -pe smp 4 -o output -e output -q all.q script.sh`

*updated 20191210*
