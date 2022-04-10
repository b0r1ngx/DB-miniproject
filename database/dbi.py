from database.db_session import Session
from database.tables.users import users
from sqlalchemy import insert
from sqlalchemy.exc import *
from psycopg2.errors import *
import re


# def insert_into_users(full_name, email, password, is_admin=False):
#     with Session() as s:
#         # "INSERT INTO users VALUES ({full_name}, {email}, {password}, {is_admin}, {created_at});
#         stmt = (insert(users).values(full_name, email, password, is_admin))
#         s.execute(stmt)
#         s.commit()


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


def get_user_id(email: str) -> int:
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


def registration(full_name, email, password) -> bool:
    """
    INSERT INTO users (full_name, email, password)
    VALUES ('{full_name}', '{email}', '{password}')
    :param full_name:
    :param email:
    :param password:
    :return: True - if successfully create account, else False
    """
    s = Session()
    try:
        s.add(users(full_name, email, password))
        s.commit()
    except:
        return False
    finally:
        s.close()
    return True


def do_user_have_access_to_other_user_photos(owner: int, viewer: int) -> dict:
    """
    Also for albums too
    :param owner:
    :param viewer:
    :return: dict: {
                "id": owner.id,
                "full_name": owner.full_name,
                "email": owner.email,
                "date": owner.created_at,
                "photos": list[of owner.photos that accces to viewer]  # TODO get photos that you have access to
            }
    """

    pass


def check_user_exist(user_id) -> bool:
    """

    :param user_id:
    :return True: - User exist
    :return False: - User not exist
    """
    pass  # TODO


def is_admin(user_id) -> bool:
    """
    hi
    :param user_id:
    :return True: - User is admin
    :return False: - User isn't admin
    """