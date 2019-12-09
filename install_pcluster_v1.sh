#!/bin/sh

uname -s

echo "READEME
- pcluster build guide on AWS - by Davis 20191208

1. launch an instance to install pcluster
- c5.large
- remember your keypair name \"eg. mykey.pem\"

2. be root
- \"sudo su -\"
- copy install_pcluster.sh into /root
- run \"chmod 667 install_pcluster.sh\"
- run \"bash install_pcluster.sh\"
- modify config file
- aws configure

3. build & check
- pcluster create <cluster_template>
- if you want to delete : \"pcluster delete <cluster_template>\"
- go to console & check your nodes
- log in master ndoes to check:
-- \"qhost\" to check your queue
-- \"df -h\" to check your volumns
-- \"qsub test.sh\" to check your cluster function
-- \"qstat -f \" to see job status" > README.md

read -t 30 -p "README created, Continue or Readme? <c/r>:  " rnext
if [ $rnext = "c" ];
then
        echo "continue..."
elif [ $rnext = "r" ];
then
        cat README.md
        echo "please run me again..."
        exit 0
else
        echo "What???"
        exit 1
fi

yum update -y

yum install python3

python3 --version

# curl -O https://bootstrap.pypa.io/get-pip.py
# python3 get-pip.py

yum install -y python3-pip.noarch

echo 'export PATH=~/.local/bin:/usr/local/bin:$PATH' >> ~/.bash_profile

source ~/.bash_profile

pip3 --version

pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

# pip3 install awscli --upgrade
# curl "https://d1vvhvl2y92vvt.cloudfront.net/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
# unzip awscliv2.zip
# sudo ./aws/install

pip3 install aws-parallelcluster --upgrade

pcluster version

read -t 30 -p "input your cluster name:  " clustername
if [ $clustername ];
then
        echo "your cluster name is: $clustername"
else
        echo "wrong clustername, try again..."
        exit 1
fi

echo "#!/bin/sh
sleep 60
echo \"test done!\"
" > /root/.parallelcluster/test.sh

echo "[aws]
aws_region_name = cn-northwest-1 # change if you want

[global]
cluster_template = $clustername # change if you want, MUST remember this name!
update_check = true
sanity_check = true

[aliases]
ssh = ssh {CFN_USER}@{MASTER_IP} {ARGS}

[cluster $clustername] # change if you changed the name of cluster_template in global settings above
key_name = newbjs # change to your keypair name
master_instance_type = c5.large  # change if you want
compute_instance_type = c5.2xlarge  # change if you want
initial_queue_size = 1  # change if you want
max_queue_size = 3  # change if you want
maintain_initial_size = true
master_root_volume_size = 300  # change if you want, 17G by default
compute_root_volume_size = 300  # change if you want, 17G by default
cluster_type = spot  # change if you want, ondemand/spot
spot_price = 1.00   # change if you want use spot as compute nodes, get latest price of specific instance in your console
base_os = alinux
custom_ami = ami-0ab8a54fbf54abb1f   # change to your customized AMI based on pcluster ami(eg. ami-0ab8a54fbf54abb1f [cn-northwest-1])
s3_read_resource = NONE
s3_read_write_resource = NONE
placement = compute
ebs_settings = custom1, custom2
vpc_settings = default

[ebs custom1]  # change or add more if you want
shared_dir = rawdata  # the dir will show in your master or compute nodes
volume_type = gp2
volume_size = 200

[ebs custom2]  # change or add more if you want
shared_dir = result
volume_type = gp2
volume_size = 200

[vpc default]
vpc_id = vpc-37a41d5e  # change to your vpc id
master_subnet_id = subnet-ee6dde87  # change to your subnet id

[scaling custom]
scaledown_idletime = 30  # change to your favorate cooldown time (min) " > /root/.parallelcluster/config

echo "now configure the pcluster config file according to your demand..."

sleep 5

vim /root/.parallelcluster/config

sleep 2

echo "configue your aws by AKSK..."

sleep 2

aws configure

read -t 30 -p "start to build pcluster? <yes/no>:  " answer
if [ $answer = "yes" ];
then
        pcluster create -c /root/.parallelcluster/config $clustername
elif [ $answer = "no" ];
then
        echo "please build manually:pcluster create $clustername"
else
        echo "What???"
        exit 1
fi
