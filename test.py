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


def login(email: str, password: str) -> bool:
    with Session() as s:
        stmt = f'''SELECT EXISTS ( 
                    SELECT * FROM (
                        SELECT * FROM users
                        WHERE users.email = '{email}'
                    ) AS u
                    WHERE u.password = '{password}');'''
        exists = s.execute(stmt)
    for i in exists:
        return i[0]



