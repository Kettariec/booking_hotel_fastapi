import smtplib
from email.message import EmailMessage
from pydantic import EmailStr
from config import settings
from bookings.model import Booking


def registration_message(email_to: EmailStr):
    email = EmailMessage()

    email["Subject"] = "Registration confirmation"
    email["From"] = settings.SMTP_USER
    email["To"] = email_to

    email.set_content(
        f"""
        <h3>Dear user! You have successfully registered in the hotel booking application!</h3>
        """,
        subtype="html"
    )

    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASS)
        server.send_message(email)


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

    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASS)
        server.send_message(email)
