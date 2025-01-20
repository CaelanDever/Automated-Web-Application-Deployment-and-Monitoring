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
