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

Step 7: Install Grafana
Add the Grafana repo and install Grafana:

sudo yum install -y https://dl.grafana.com/oss/release/grafana-9.4.7-1.x86_64.rpm
sudo systemctl start grafana-server
sudo systemctl enable grafana-server

<img width="452" alt="bf" src="https://github.com/user-attachments/assets/d5efd1ac-c663-4133-b926-6d57f66e60d4" />

Access Grafana at http://45.79.201.189:3000 (default login: admin/admin).





# Phase 5: Centralized Authentication
Step 9: Set Up LDAP
Install OpenLDAP:

sudo yum install -y openldap openldap-servers openldap-clients
sudo systemctl start slapd
sudo systemctl enable slapd

<img width="453" alt="cff" src="https://github.com/user-attachments/assets/eb09604d-a58d-4230-9abf-cb5fc94bf654" />

Add LDAP users:

ldapadd -x -D "cn=Manager,dc=example,dc=com" -W -f users.ldif

# Phase 6: Scripting and Debugging

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

# Phase 7: Virtualization and Scaling

In this phase, you'll use Linode's virtualization tools and simple scaling strategies to expand your infrastructure. This will include deploying additional servers and automating their setup for load balancing.
