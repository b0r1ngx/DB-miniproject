import re

EMAIL_PATTERN = re.compile('^[A-Za-z0-9.+_-]+@[A-Za-z0-9._-]+\.[a-zA-Z]*$')

def email_is_valid(email: str) -> bool:
    if EMAIL_PATTERN.match(email):
        return True
    return False