import smtplib
from email.message import EmailMessage
from pydantic import EmailStr
from config import settings
from bookings.model import Booking
from datetime import datetime, timedelta
import jwt


def send_message(message: EmailMessage):
    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASS)
        server.send_message(message)


def generate_email_verification_token(email: EmailStr):
    expiration = timedelta(hours=24)
    return jwt.encode({"sub": email, "exp": datetime.utcnow() + expiration}, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def registration_message(email_to: EmailStr):
    token = generate_email_verification_token(email_to)
    verification_link = f"{settings.FRONTEND_URL}/auth/verify-email?token={token}"
    email = EmailMessage()

    email["Subject"] = "Confirm your registration"
    email["From"] = settings.SMTP_USER
    email["To"] = email_to

    email.set_content(
        f"""
        <h3>Dear user! Please confirm your registration by clicking the link below:</h3>
        <a href="{verification_link}">Confirm Registration</a>
        """,
        subtype="html"
    )

    send_message(email)


def booking_message(booking: Booking, email_to: EmailStr):
    email = EmailMessage()

    email["Subject"] = "Confirm booking"
    email["From"] = settings.SMTP_USER
    email["To"] = email_to

    email.set_content(
        f"""
        <h3>You have successfully booked the room {booking.room_name} in the hotel {booking.hotel_name}!</h3>
        <h3>Check-in date: {booking.date_from}</h3>
        <h3>Check-out date: {booking.date_to}</h3>
        <h3>Total cost: {booking.total_cost} rubles</h3>
        <h3>We are waiting for you, dear guest!</h3>
        """,
        subtype="html"
    )

    send_message(email)
