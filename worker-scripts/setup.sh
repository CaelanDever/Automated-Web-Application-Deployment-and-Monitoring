#!/bin/bash
sudo yum update -y
sudo yum install -y epel-release
sudo yum install -y yum-utils docker-ce docker-ce-cli containerd.io

sudo systemctl start docker
sudo systemctl enable docker
