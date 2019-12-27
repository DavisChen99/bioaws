#!/bin/sh

uname -s

read -t 30 -p "Continue or Readme? <c/r>:  " rnext
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

yum install -y python3

python3 --version

# curl -O https://bootstrap.pypa.io/get-pip.py
# python3 get-pip.py

yum install -y python3-pip.noarch

echo 'export PATH=~/.local/bin:/usr/local/bin:$PATH' >> ~/.bash_profile

sleep 1

source ~/.bash_profile

pip3 --version

# pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
# pip3 install awscli --upgrade
# curl "https://d1vvhvl2y92vvt.cloudfront.net/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
# unzip awscliv2.zip
# sudo ./aws/install

pip3 install aws-parallelcluster --upgrade -i https://pypi.tuna.tsinghua.edu.cn/simple

echo "your pcluster version is:"
pcluster version

sleep 1

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

read -t 30 -p "start to configure? <yes/no>:  " configcheck
if [ $configcheck = "yes" ];
then
echo "[aws]
aws_region_name = cn-northwest-1 # change if you want

[global]
cluster_template = $clustername # change if you want
update_check = true
sanity_check = true

[aliases]
ssh = ssh {CFN_USER}@{MASTER_IP} {ARGS}

[cluster $clustername] # keep the same as the name of cluster_template in global settings above
key_name = newbjs # MUST change to your keypair name
#master_instance_type = c5.large  # change to c/m/r series, t2.micro by default
compute_instance_type = c5.2xlarge  # change if you want
initial_queue_size = 1  # change if you want
max_queue_size = 10  # change if you want
maintain_initial_size = true
master_root_volume_size = 30  # change if you want, 17G by default
compute_root_volume_size = 30  # change if you want, 17G by default
cluster_type = spot  # change if you want, ondemand/spot
spot_price = 1.30   # change if you want use spot as compute nodes, get latest price of specific instance in your console
base_os = alinux
custom_ami = ami-05038e0c41061b799 #2.5.1ami   # change to your customized AMI based on pcluster ami(eg. ami-0ab8a54fbf54abb1f [cn-northwest-1]/ ami-02d8c4f46ddaa963f [cn-north-1])
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

vim /root/.parallelcluster/config 

elif [ $configcheck = "no" ];
then
        echo "skip...configure manually： /root/.parallelcluster/config"
else
        echo "What???"
        exit 1

fi

echo "configure your aws by AKSK..."

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
