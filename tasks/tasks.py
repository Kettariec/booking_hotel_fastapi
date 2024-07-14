import smtplib
from email.message import EmailMessage
from pydantic import EmailStr
from config import settings


def send_mail():
    email = EmailMessage()

    email["Subject"] = "Confirm booking"
    email["From"] = settings.SMTP_USER
    email["To"] = settings.SMTP_USER

    email.set_content(
        f"""
        <h1> You are booking!</h1>
        You got hotel!
        """,
        subtype="html"
    )
    return email


def send_booking():
    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASS)
        server.send_message(send_mail())
