# actions.py
import requests, os, smtplib, json
from email.mime.text import MIMEText
from datetime import datetime

SLACK_WEBHOOK = os.getenv("SLACK_WEBHOOK_URL")

def post_slack(message, channel=None):
    if not SLACK_WEBHOOK:
        return {"ok":False, "error":"no webhook set"}
    payload = {"text": message}
    r = requests.post(SLACK_WEBHOOK, json=payload, timeout=10)
    return {"ok": r.status_code==200, "status_code": r.status_code, "text": r.text}

def send_email(to_address, subject, body):
    smtp = os.getenv("ALERT_EMAIL_SMTP")
    user = os.getenv("ALERT_EMAIL_USER")
    pwd = os.getenv("ALERT_EMAIL_PASS")
    if not smtp or not user or not pwd:
        return {"ok":False, "error":"missing email config"}
    host, port = smtp.split(":")
    port = int(port)
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = user
    msg["To"] = to_address
    server = smtplib.SMTP(host, port)
    server.starttls()
    server.login(user, pwd)
    server.sendmail(user, [to_address], msg.as_string())
    server.quit()
    return {"ok":True}

def save_report_text(summary, path="reports/report-{}.txt".format(datetime.now().strftime("%Y%m%d-%H%M%S"))):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf8") as f:
        f.write(summary)
    return {"ok":True, "path":path}
