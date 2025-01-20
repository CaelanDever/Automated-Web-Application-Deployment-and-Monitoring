# Automated Web Application Deployment and Monitoring

This project demonstrates the complete workflow for deploying, automating, monitoring, and scaling a Flask-based To-Do List Web Application using Linode servers. By leveraging essential DevOps tools and practices, the project showcases an end-to-end solution, from initial server setup to advanced scaling and monitoring.

# 🚀 Key Features

Automated Server Setup: Shell scripts automate the installation and configuration of essential tools like Docker and OpenLDAP.

 Containerized Application Deployment: The web application is containerized using Docker, ensuring consistency across environments.
Infrastructure as Code (IaC): Ansible is used to manage and deploy the app across multiple servers.

Scalable Architecture: Easily add new servers and integrate them with the existing infrastructure, including load balancing with HAProxy.

Comprehensive Monitoring: Prometheus and Grafana provide real-time metrics and dashboards for proactive monitoring.

Disk Usage Alert System: A Python script monitors disk space and sends email alerts for threshold breaches.

# 🛠️ Technologies Used

Infrastructure: Linode CentOS 9 Stream servers

Automation: Shell scripting, Ansible

Containerization: Docker

Monitoring: Prometheus, Grafana

Authentication: OpenLDAP

Load Balancing: HAProxy

Programming Languages: Python, Bash


📖 Workflow Overview


Phase 1: Basic Setup

Create and configure Linode servers.

Install and configure Docker to run the Flask web application.


Phase 2: Automation

Automate server setup and app deployment with Bash scripts.


Phase 3: Monitoring

Install Prometheus and Grafana for monitoring infrastructure and applications.


Phase 4: Centralized Authentication

Set up OpenLDAP for user authentication and management.


Phase 5: Disk Monitoring

Python script monitors disk usage and sends email alerts for high usage.


Phase 6: Scaling

Add new Linode servers, deploy the app with Ansible and update HAProxy.

_________________________________________________________________________________________________________________

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
sudo yum-config-manager --add-repo 
https://download.docker.com/linux/centos/docker-ce.repo
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

Step 7: Install Grafana

Add the Grafana repo and install Grafana:

sudo yum install -y https://dl.grafana.com/oss/release/grafana-9.4.7-1.x86_64.rpm
sudo systemctl start grafana-server
sudo systemctl enable grafana-server

<img width="452" alt="bf" src="https://github.com/user-attachments/assets/d5efd1ac-c663-4133-b926-6d57f66e60d4" />

Access Grafana at http://45.79.201.189:3000 (default login: admin/admin).

# Phase 4: Centralized Authentication

Step 1: Set Up LDAP
Install OpenLDAP:

sudo yum install -y openldap openldap-servers openldap-clients
sudo systemctl start slapd
sudo systemctl enable slapd

<img width="453" alt="cff" src="https://github.com/user-attachments/assets/eb09604d-a58d-4230-9abf-cb5fc94bf654" />

Add LDAP users:

ldapadd -x -D "cn=Manager,dc=example,dc=com" -W -f users.ldif

# Phase 5: Scripting and Debugging

Write Python scripts to manage infrastructure and debug issues effectively.

Step 1: Understand the Goal

We are writing a Python script that:

Checks how much disk space is used on your Linux server.

Sends an email alert if usage exceeds a certain percentage.

Create a new Python script file:
nano monitor_disk_usage.py

Add this code:

import os
import smtplib
from email.mime.text import MIMEText
import shutil

def check_disk_usage(path="/"):
    total, used, free = shutil.disk_usage(path)
    percent_used = (used / total) * 100
    return percent_used, free

def send_email_alert(subject, body, to_email):
    from_email = "your_email@example.com"
    smtp_server = "smtp.example.com"
    smtp_port = 587
    password = "your_password"
    
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = from_email
    msg["To"] = to_email
    
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(from_email, password)
            server.sendmail(from_email, to_email, msg.as_string())
            print("Alert email sent successfully.")
    except Exception as e:
        print(f"Error sending email: {e}")

def monitor_disk_usage(threshold=80, path="/", alert_email="admin@example.com"):
    usage, free_space = check_disk_usage(path)
    if usage > threshold:
        subject = f"Disk Usage Alert: {usage:.2f}% Used"
        body = (f"Warning! Disk usage on {path} has exceeded {threshold}%.\n"
                f"Current usage: {usage:.2f}%\nFree space: {free_space / (1024**3):.2f} GB.")
        send_email_alert(subject, body, alert_email)

if __name__ == "__main__":
    path_to_monitor = "/"  # Root directory
    usage_threshold = 80  # Alert if usage exceeds 80%
    admin_email = "admin@example.com"
    monitor_disk_usage(threshold=usage_threshold, path=path_to_monitor, alert_email=admin_email)


<img width="451" alt="grr" src="https://github.com/user-attachments/assets/16724ab6-0565-47fc-8308-029b962dbd1a" />

Step 4: Update Email Settings

Open the script again:

vimmonitor_disk_usage.py

Update the following placeholders:

your_email@example.com: Replace with your email address (e.g., myemail@gmail.com).
smtp.example.com: Replace with your email provider's SMTP server (e.g., Gmail: smtp.gmail.com).
your_password: Replace with your email password or an app-specific password.
admin@example.com: Replace with the email that should receive alerts.
Save and exit the script.

<img width="455" alt="fc" src="https://github.com/user-attachments/assets/9b96cd1c-9a83-4112-9b25-5ca6f2f82267" />


Step 5: Test the Script

Run the script manually

python3 monitor_disk_usage.py

Force a test alert by temporarily setting the threshold to 0

Open the script:

nano monitor_disk_usage.py

Find this line:

usage_threshold = 80

Change 80 to 0 and save.
Run the script again. You should receive a test email alert.

<img width="455" alt="fa" src="https://github.com/user-attachments/assets/7cdae257-5e5f-4607-aaf6-a5cc7a017731" />

I purposefully did not put in my real password for security purposes.

Step 6: Automate the Script

Open the crontab editor:

crontab -e

Add this line to run the script every hour:

0 * * * * /usr/bin/python3 /home/root/monitor_disk_usage.py

<img width="428" alt="gq" src="https://github.com/user-attachments/assets/3041f403-2a83-42d2-a585-1a6b2aeb7b79" />

Save and exit. wq!

Step 7: Monitor and Debug

If no emails are received:

Check your email settings and credentials.

Verify the server has internet access.

Test by filling the disk or lowering the threshold.

# Phase 6: Scaling – Add More Servers

This step walks you through scaling your infrastructure by adding new Linode servers, configuring them, and using Ansible to deploy your application across these new servers in detail.

Add More Servers

1. Create New Linode Servers

Log in to Linode:

Go to your Linode dashboard.

Click Create > Linode.

Configure Your New Linodes:

Image: Select CentOS 9 Stream.
Region: Choose the same region as your existing servers.
Plan: Select the desired size (e.g., Shared CPU 1GB).
Label: Name your servers (e.g., todo-app-server-A and todo-app-server-B).
Root Password: Set a secure password for the root user.
Note the IP Addresses:

Once created, note the public IP addresses of the new servers. These will be used in the Ansible inventory file.

<img width="461" alt="vsd" src="https://github.com/user-attachments/assets/2887867a-bf06-411a-b3c9-8761d468587e" />


2. Prepare the New Servers
   
Before using Ansible, ensure basic connectivity to the new servers.

Access the New Servers via SSH:

From your local machine, SSH into each new server:

ssh root@<NEW_SERVER_IP>

3. Update the Ansible Inventory File

Edit the inventory.ini File:

Open your existing inventory file:

vim inventory.ini

Add the new servers under the appropriate group:

[todo_vms]
vm1 ansible_host=<EXISTING_SERVER_1_IP>
vm2 ansible_host=<<NEW_SERVER_2_IP>
vm3 ansible_host=<NEW_SERVER_3_IP>


<img width="193" alt="gff" src="https://github.com/user-attachments/assets/1a0149bc-1863-4ce2-9acc-6604c41b086b" />

Test Ansible Connectivity:

Verify Ansible can connect to all servers

ansible -i inventory.ini all -m ping

<img width="413" alt="ve" src="https://github.com/user-attachments/assets/9c3ea2be-0c32-4ad2-90ef-2250fdbf95e8" />

Successful output should show

vm1 | SUCCESS => {"changed": false, "ping": "pong"}
vm2 | SUCCESS => {"changed": false, "ping": "pong"}
vm3 | SUCCESS => {"changed": false, "ping": "pong"}

4. Update the Ansible Playbook (deploy.yml)

Ensure the playbook is configured to handle new servers dynamically.

Review the Playbook: Open your deploy.yml file:

vim deploy.yml

Structure of the Playbook: Ensure it installs Docker, pulls the app, and starts the container:

---
- name: Deploy To-Do List App
  hosts: todo_vms
  become: yes
  tasks:
    - name: Update all packages
      yum:
        name: "*"
        state: latest
        update_cache: yes

    - name: Install Docker
      yum:
        name: docker-ce
        state: present

    - name: Start Docker service
      service:
        name: docker
        state: started
        enabled: yes

    - name: Pull and Run the To-Do List App container
      shell: |
        docker pull todo-app:latest
        docker run -d -p 5000:5000 --name todo-app todo-app
      args:
        creates: /var/run/docker.sock

  <img width="427" alt="ge" src="https://github.com/user-attachments/assets/5b7b4c2f-33c7-4fe1-a7a0-b447e73572d7" />

5. Deploy the Application

Run the Ansible playbook to configure and deploy the app across all servers, including the new ones.

Run the Playbook:

ansible-playbook -i inventory.ini deploy.yml


<img width="451" alt="few" src="https://github.com/user-attachments/assets/82cb2170-056c-4a14-b0c9-2de6253cf98d" />


Monitor the Output:

Ansible will sequentially connect to each server and run the tasks.
Look for ok, changed, or success messages for each task

TASK [Update all packages] *********************************************
ok: [vm1]
ok: [vm2]
ok: [vm3]


TASK [Install Docker] **************************************************
changed: [vm2]
changed: [vm3]

TASK [Update all packages] *********************************************
ok: [vm1]
ok: [vm2]
ok: [vm3]


TASK [Install Docker] **************************************************
changed: [vm2]
changed: [vm3]

6. Verify Deployment

Check docker image is running:

![image](https://github.com/user-attachments/assets/18500e67-4a96-4a3f-bab7-9c821e15cb59)


Check App Availability:

Visit http://<NEW_SERVER_IP>:5000 in your browser for each new server.

<img width="529" alt="cvs" src="https://github.com/user-attachments/assets/6ba66cbd-35e9-4d93-8cb3-58ebb9f82607" />

Check Docker Containers:

SSH into one of the new servers:

ssh root@<NEW_SERVER_IP>

Run:

docker ps

Output should show the running todo-app container.

<img width="452" alt="gtt" src="https://github.com/user-attachments/assets/61d32319-de9c-4a54-91dc-dc2ac971ce71" />


Test Across All Servers:

Confirm the app is reachable and working on all new servers.

<img width="281" alt="tq" src="https://github.com/user-attachments/assets/055bfb3e-e5c5-4d2b-abde-fe7561263c89" />


7. Update Load Balancer

If you’re using HAProxy or a similar load balancer, update its configuration to include the new servers.

Edit the HAProxy Config:

sudo vim /etc/haproxy/haproxy.cfg

Add the new servers under the backend section:

backend http_back
    balance roundrobin
    server web1 <EXISTING_SERVER_1_IP>:5000 check
    server web2 <EXISTING_SERVER_2_IP>:5000 check
    server web3 <NEW_SERVER_3_IP>:5000 check

<img width="402" alt="grg" src="https://github.com/user-attachments/assets/1993a32f-961b-4e94-a2f8-fa389bb3264f" />

   
Reload HAProxy:

sudo systemctl reload haproxy

<img width="323" alt="yw" src="https://github.com/user-attachments/assets/1184e047-1cef-46e7-a7fb-8139ef3c40a2" />


Test Load Balancer:

Visit the load balancer’s IP (http://<HAPROXY_IP>).
Requests should round-robin across all four servers.

<img width="266" alt="cass" src="https://github.com/user-attachments/assets/b5aa7821-7dda-4b81-8816-0b3ba95a1b37" />


Summary of Results

New Linode servers are created and configured.

Ansible deploys the app and ensures consistent configuration across all 
servers.

The load balancer and monitoring systems are updated to include the new servers.

The infrastructure is scaled efficiently, with all servers contributing to the app's availability.
