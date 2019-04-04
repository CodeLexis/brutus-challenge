from flask import current_app as app
from flask_mail import Mail, Message


def get_previous_login_attempt(ip_address):
    return


def handle_failed_login(email, ip_address):
    send_email(
        email,
        subject='Security Alert',
        body='A login attempt was made from %s' % ip_address
    )


def send_email(email, subject, body, attachments=None):
    attachments = None or []

    msg = Message(
        subject=subject,
        sender=app.config['MAIL_SENDER'],
        recipients=[email]
    )
    msg.body = body

    mail = Mail(app)
    mail.send(msg)
