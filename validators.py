import re


def validate_password(password):
    password_pattern = r'^[A-Za-z0-9_\-@#$%]+$'

    if len(password) < 16:
        return False

    return True
