sudo yum update -y
# install git
sudo yum install git -y
# install docker
sudo yum install docker -y
sudo service docker start
sudo usermod -a -G docker ec2-user

