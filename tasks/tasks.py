import smtplib
from email.message import EmailMessage
from pydantic import EmailStr
from config import settings
from bookings.model import Booking


def booking_message(booking: Booking,email_to: EmailStr):
    email = EmailMessage()

    email["Subject"] = "Confirm booking"
    email["From"] = settings.SMTP_USER
    email["To"] = email_to

    email.set_content(
        f"""
        <h1> You are booking!</h1>
        {booking}
        """,
        subtype="html"
    )
    return email


def send_booking_message(booking: Booking, email_to: EmailStr):
    message = booking_message(booking, email_to)
    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASS)
        server.send_message(message)
