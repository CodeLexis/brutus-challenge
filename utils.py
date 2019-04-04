from datetime import datetime
from flask import current_app as app
from flask_mail import Mail, Message
import pymongo

from models import LoginActivity
from constants import FAILURE_STATUS


def check_if_ip_can_login(ip_address):
    current_timestamp = datetime.now().timestamp()

    previous_attempts = get_previous_login_attempts(ip_address)

    failed_count = previous_attempts['failed']
    records = previous_attempts['records']

    if failed_count == app.config['MAX_LOGIN_ATTEMPTS']:
        last_activity = records[0]
        seconds_since_last_login_activity = (
            current_timestamp - last_activity['created_at'].timestamp()
        )

        if (seconds_since_last_login_activity <
                app.config['LOGIN_REST_PERIOD_SECONDS']):
            return False

    return True


def get_previous_login_attempts(ip_address):
    cursor = LoginActivity.find({
        'ip_address': ip_address
    }).sort(
        [('_id', pymongo.DESCENDING)]
    ).limit(
        app.config['MAX_LOGIN_ATTEMPTS']
    )

    cursor_2 = LoginActivity.find({
        'ip_address': ip_address,
        'status': FAILURE_STATUS
    }).sort(
        [('_id', pymongo.DESCENDING)]
    ).limit(
        app.config['MAX_LOGIN_ATTEMPTS']
    )

    return {
        'records': [obj for obj in cursor],
        'failed': len(
            [obj for obj in cursor_2])
    }


def handle_failed_login(email, ip_address):
    previous_attempts = get_previous_login_attempts(ip_address)
    failed_count = previous_attempts['failed']

    if failed_count == app.config['MAX_LOGIN_ATTEMPTS'] - 1:
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
