from database.db_session import Session
from database.tables.users import users
from sqlalchemy import insert
import datetime


def insert_into_values(full_name, email, password, is_admin=False, created_at=datetime.now()):
    with Session as s:
        # "INSERT INTO users VALUES ({full_name}, {email}, {password}, {is_admin}, {created_at});
        stmt = (insert(users).values(full_name, email, password, is_admin, created_at))
        s.commit()