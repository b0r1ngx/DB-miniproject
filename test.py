from database.db_session import Session
from database.tables.users import users
from sqlalchemy import insert


def insert_into_values(full_name, email, password, is_admin=False):
    with Session as s:
        # "INSERT INTO users VALUES ({full_name}, {email}, {password}, {is_admin}, {created_at});
        stmt = (insert(users).values(full_name, email, password, is_admin))
        s.commit()