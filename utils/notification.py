import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_slack_alert(vulnerabilities):
    slack_url = "https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK"
    message = "High-priority vulnerabilities:\n" + "\n".join([f"{vuln.cve_id} - Score: {vuln.priority_score}" for vuln in vulnerabilities])
    requests.post(slack_url, json={"text": message})

def send_email_alert(vulnerabilities):
    sender_email = "your_email@example.com"
    recipient_email = "recipient@example.com"
    subject = "High-Priority Vulnerabilities Alert"
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    body = "High-priority vulnerabilities:\n" + "\n".join([f"{vuln.cve_id} - Score: {vuln.priority_score}" for vuln in vulnerabilities])
    msg.attach(MIMEText(body, 'plain'))
    server = smtplib.SMTP('smtp.example.com', 587)
    server.starttls()
    server.login(sender_email, "your_password")
    server.sendmail(sender_email, recipient_email, msg.as_string())
    server.quit()
