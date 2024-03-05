import smtplib, ssl
from email.mime.text import MIMEText
from email.message import EmailMessage

from pydantic import EmailStr

from app.config import settings


def create_bookings_confirmation(
        booking: dict,
        email_to: EmailStr
):
    email = EmailMessage()
    email["Subject"] = "Подтверждение бронирования"
    email["From"] = settings.SMTP_USER
    email["To"] = email_to

    html = f"""
    <html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Подтверждение бронирования отеля</title>
</head>
<body>
<div class="container">
    <h1>Подтверждение бронирования отеля</h1>
    <p>Благодарим вас за выбор нашего отеля. Ваше бронирование было успешно подтверждено.</p>
    <h2>Детали бронирования:</h2>
    <ul>
        <li><strong>Номер:</strong> {booking["name"]}</li>
        <li><strong>Номер брони:</strong> {booking["id"]}</li>
        <li><strong>Дата заезда:</strong> {booking["date_from"]}</li>
        <li><strong>Дата выезда:</strong> {booking["date_to"]}</li>
        <li><strong>Цена:</strong> {booking["total_cost"]} руб.</li>
    </ul>
    <p>Если у вас возникнут какие-либо вопросы или требуется дополнительная информация, не стесняйтесь связаться с
        нами.</p>
    <p>Желаем вам приятного пребывания!</p>
    <p>С наилучшими пожеланиями,<br>Команда Отеля</p>
</div>
</body>
</html>
    """

    email.set_content(html, subtype="html")

    return email
