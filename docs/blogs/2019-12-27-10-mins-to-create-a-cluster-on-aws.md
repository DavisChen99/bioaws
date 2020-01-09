## pcluster quick-build within 10 min

### launch an instance to install pcluster (v2.5.1)
- `eg. t2.micro`
- remember your keypair name `eg. mykey.pem`
- launch & login

### install packages & launch cluster
- `wget https://github.com/DavisChen99/awspac/archive/master.zip`
- `unzip awspac-master.zip && cd awspac-master`
- refer to [doc](https://aws-parallelcluster.readthedocs.io/en/latest/configuration.html#scheduler)
- add permission `chmod 667 install_pcluster_v1.sh`
- run `sudo bash install_pcluster_v1.sh`, try again if you meet HTTPS connect problem - usually network issue.

### build manually (after first build)
- `sudo su -`
- `cd /root/.parallelcluster`
- `vim config` edit as you want
- `aws configure` with your AKSK keys
- `pcluster <create/delete> <cluster_template>`

### check service
- go to aws console & check your nodes
- log in master nodes to check:
  * `qhost` to check your queue
  * `df -h` to check your volumns
  * `qsub test.sh` to check your cluster function
  * `qstat -f` to see job status
- submit your jobs using command like `qsub -cwd -S /bin/bash -V -l vf=2G -pe smp 4 -o output -e output -q all.q yourscript.sh`

### for debug
- `vi ~/.bashrc`
- add `export SGE_ROOT=/opt/sge`
- add `PATH=/opt/sge/bin:/opt/sge/bin/lx-amd64:/opt/amazon/openmpi/bin:$PATH`
- `source ~/.bashrc`
- `sudo /etc/init.d/sgemaster.p6444 <start/stop/restart>`
