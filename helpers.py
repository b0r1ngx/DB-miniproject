import re

EMAIL_PATTERN = re.compile('[^@]+@[^@]+\.[^@]+')


def email_is_valid(email: str) -> bool:
    if EMAIL_PATTERN.match(email):
        return True
    return False