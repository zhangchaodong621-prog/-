from __future__ import annotations

import os
import smtplib
from email.message import EmailMessage


def send_gmail_smtp(subject: str, body: str) -> None:
    host = os.environ["SMTP_HOST"]
    port = int(os.getenv("SMTP_PORT", "587"))
    user = os.environ["SMTP_USER"]
    password = os.environ["SMTP_PASS"]
    mail_to = os.environ["MAIL_TO"]

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = user
    msg["To"] = mail_to
    msg.set_content(body)

    with smtplib.SMTP(host=host, port=port, timeout=30) as s:
        s.ehlo()
        s.starttls()
        s.login(user, password)
        s.send_message(msg)

