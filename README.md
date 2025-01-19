# Automated-Web-Application-Deployment-and-Monitoring

This project demonstrates a complete workflow to deploy, automate, monitor, and scale a web application using **Linode servers**. It contains hands-on experience with essential DevOps tools and practices, including:

- **Docker**: For containerizing a Python Flask application.
- **Ansible**: For automating server configuration and application deployment.
- **Prometheus and Grafana**: For monitoring and visualizing system and application metrics.
- **Fluentd**: For centralized logging.
- **OpenLDAP**: For centralized authentication.
________________________________________________________________________________________________________________________________________________________________________

# Phase 1: Set Up the Basics

Step 1: Create and Access Linode Servers

Log in to your Linode account and create two CentOS 9 Stream servers.

After deployment, note the IP addresses of your servers.

<img width="434" alt="dwwd" src="https://github.com/user-attachments/assets/c7a103d8-23f7-4f17-8f51-bec683890398" />

SSH into the servers via MobaXterm:
ssh root@45.79.201.189

Step 2: Update and Configure Servers

Run these commands on both servers:

Update the system
sudo yum update -y

Install basic tools
sudo yum install -y epel-release vim wget curl

<img width="480" alt="vc" src="https://github.com/user-attachments/assets/fdb5fef6-8042-40ea-b54b-c60becd9521c" />

Step 3: Install Docker
Install Docker:

sudo yum install -y yum-utils
sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
sudo yum install -y docker-ce docker-ce-cli containerd.io

<img width="481" alt="acs" src="https://github.com/user-attachments/assets/63887e0b-4296-4ae1-ad07-a53d7c66253c" />

Start and enable Docker:

sudo systemctl start docker
sudo systemctl enable docker

Verify Docker installation:

docker --version

<img width="260" alt="eq" src="https://github.com/user-attachments/assets/141bdaf3-c1ea-4956-94a9-bd600a02caea" />

Step 4: Deploy a Flask "To-Do List" App

On one server, create the project directory:

mkdir -p /opt/todo-app
cd /opt/todo-app

Create the Dockerfile:

vim Dockerfile

Add the following content:

FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app.py .
CMD ["python", "app.py"]

<img width="222" alt="cf" src="https://github.com/user-attachments/assets/2b7e7e83-6107-42b1-8ca9-4905b3a6f85e" />

Create the Flask app (app.py) and dependencies file (requirements.txt):

vim app.py

Add:

from flask import Flask
app = Flask(__name__)

@app.route("/")
def home():
    return "Welcome to the To-Do List App!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


<img width="276" alt="gf" src="https://github.com/user-attachments/assets/7608780f-a610-44b8-b338-be70a117f062" />

vim requirements.txt

Add:

flask

Build and run the app:

docker build -t todo-app .
docker run -d -p 5000:5000 todo-app 


<img width="481" alt="ef" src="https://github.com/user-attachments/assets/4bdb135d-d235-47a9-a254-7f95af451417" />

Test the app by visiting http://45.79.201.189:5000.

<img width="452" alt="yt" src="https://github.com/user-attachments/assets/9b1a3d1b-f6f9-448f-b167-9b45c5f35d42" />

# Phase 2: Automate Setup with Scripts

Step 5: Write Bash Automation Scripts
Create a script to automate server setup (setup.sh):

vim setup.sh

Add:

#!/bin/bash
sudo yum update -y
sudo yum install -y epel-release
sudo yum install -y yum-utils docker-ce docker-ce-cli containerd.io

sudo systemctl start docker
sudo systemctl enable docker

<img width="432" alt="tw" src="https://github.com/user-attachments/assets/cdb81d0e-bb03-4aa8-981c-d048fba751f8" />

Make the script executable:
chmod +x setup.sh

Run the script:

./setup.sh

<img width="486" alt="eff" src="https://github.com/user-attachments/assets/f8203771-6fbe-4ae2-8e0d-1c5f7157827d" />

# Phase 3: Monitoring and Alerting

Step 6: Install Prometheus
On the first server, download and install Prometheus:

sudo useradd --no-create-home prometheus
sudo mkdir /etc/prometheus /var/lib/prometheus
sudo chown prometheus:prometheus /etc/prometheus /var/lib/prometheus

curl -LO https://github.com/prometheus/prometheus/releases/download/v2.47.0/prometheus-2.47.0.linux-amd64.tar.gz
tar -xvf prometheus-*.tar.gz
sudo cp prometheus-2.47.0.linux-amd64/prometheus /usr/local/bin/

<img width="486" alt="vv" src="https://github.com/user-attachments/assets/ebc287ac-ca63-49fd-b137-241b4e28026f" />

Create a Prometheus service file:

sudo vim /etc/systemd/system/prometheus.service

Add:

[Unit]
Description=Prometheus
Wants=network-online.target
After=network-online.target

[Service]
User=prometheus
ExecStart=/usr/local/bin/prometheus --config.file=/etc/prometheus/prometheus.yml

[Install]
WantedBy=multi-user.target

<img width="486" alt="vaa" src="https://github.com/user-attachments/assets/43b68800-1f70-4949-841a-da478a5140d1" />

Reload services and start Prometheus:

sudo systemctl daemon-reload
sudo systemctl start prometheus
sudo systemctl enable prometheus


<img width="482" alt="vf" src="https://github.com/user-attachments/assets/3e07de7f-ef40-437b-b6f1-3111752f645b" />

Access Prometheus at http://45.79.201.189:9090

