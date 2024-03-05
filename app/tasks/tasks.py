from pathlib import Path

from pydantic import EmailStr

from app.config import settings
from app.tasks.celery import celery
from PIL import Image

from app.tasks.emailtemplates import create_bookings_confirmation

import smtplib


@celery.task
def process_pic(
        path: str,
):
    img_path = Path(path)
    im = Image.open(img_path)
    img_resized_1000_500 = im.resize((1000, 500))
    img_resized_200_100 = im.resize((200, 100))
    img_resized_1000_500.save(f"app/static/images/resized_1000_500_{img_path.name}")
    img_resized_200_100.save(f"app/static/images/resized_200_100_{img_path.name}")



@celery.task
def send_booking_confirmation_email(
    booking: dict,
    email_to: EmailStr,
):

    msg_content = create_bookings_confirmation(booking, email_to)

    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASS)
        server.send_message(msg_content)


