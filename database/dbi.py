from database.db_session import Session
from database.tables.users import users
from sqlalchemy import insert
import re


def insert_into_users(full_name, email, password, is_admin=False):
    with Session() as s:
        # "INSERT INTO users VALUES ({full_name}, {email}, {password}, {is_admin}, {created_at});
        stmt = (insert(users).values(full_name, email, password, is_admin))
        s.execute(stmt)
        s.commit()


def login(email: str, password: str) -> int:
    """
    :param email: user email
    :param password: user password
    :return: -1 - reserved (for if email found, but password is wrong);
              0 - means this email and password don't;
              id - id from users table
    """
    with Session() as s:
        stmt = f'''SELECT u.id FROM (
                        SELECT * FROM users
                        WHERE users.email = '{email}'
                    ) AS u
                    WHERE u.password = '{password}';'''
        id = s.execute(stmt)
    for id in id:
        return id[0]


def get_user_id(email:str) -> int:
    """
    Also can be used on registration() when need to check if user exists
    :param email:
    :return:
    """
    with Session() as s:
        stmt = f'''SELECT * FROM users
                   WHERE users.email = '{email}\''''
        exists = s.execute(stmt)
    for i in exists:
        return i[0]
