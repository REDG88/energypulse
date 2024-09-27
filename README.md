# energypulse
hackathon

1. Create an EC2 with the following characteristics

amazon linux 2

t3.medium

user data:
#!/bin/bash
yum update -y
yum install git -y
git — version
git config — global user.name “energypulse”
git config — global user.email “duarterodrigoco@hotmail.com”
amazon-linux-extras install nginx1 python3 -y
pip3 install flask boto3 pandas
systemctl enable nginx
systemctl start nginx
cd /home/ec2-user
mkdir energypulse
# Clone or fetch your app from S3 or GitHub
git clone https://github.com/REDG88/energypulse.git
python3 energy_pulse_agent.py &
