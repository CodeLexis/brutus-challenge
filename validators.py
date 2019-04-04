import re


def validate_password(password):
    password_pattern = r'^([A-Za-z0-9_\-@#$%]){16,}$'
    password_pattern_2 = r'^.*\d.*.*\d.*.*\d.*'
    password_pattern_3 = r'^[A-Z][A-Z].*'
    password_pattern_4 = r'^.*[-@#$%].*.*[-@#$%].*'

    if not re.match(password_pattern, password):
        raise ValueError('Invalid password')

    if not re.match(password_pattern_2, password):
        raise ValueError('Invalid password')

    if not re.match(password_pattern_3, password):
        raise ValueError('Invalid password')

    if not re.match(password_pattern_4, password):
        raise ValueError('Invalid password')

    return True
