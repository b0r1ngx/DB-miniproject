import re
from hashlib import sha3_512

EMAIL_PATTERN = re.compile('^[A-Za-z0-9.+_-]+@[A-Za-z0-9._-]+\.[a-zA-Z]*$')


def email_is_valid(email: str) -> bool:
    if EMAIL_PATTERN.match(email):
        return True
    return False


def encode_password(password: str) -> str:
    return sha3_512(password.encode()).hexdigest()
