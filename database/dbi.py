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
    for i in id:
        return i[0]


def get_user_id(email: str) -> int:
    """
    Also can be used on registration() when need to check if user exists
    :param email:
    :return:
    """
    with Session() as s:
        stmt = f'''SELECT * FROM users
                   WHERE users.email = '{email}\''''
        id = s.execute(stmt)
    for i in id:
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


def do_user_have_access_to_other_user_photos(owner_id: int, viewer_id: int) -> dict:
    """What photos can viewer see at owner (someone)

Also for albums too
    :param owner_id:
    :param viewer_id:
    :return: dict: {
                "id": owner.id,
                "full_name": owner.full_name,
                "email": owner.email,
                "date": owner.created_at,
                "photos": list[of owner.photos that acccess to viewer]  # TODO get photos that you have access to
            }"""
    # with Session() as s:
    #     s.query(photos)
    #     photos = s.execute(stmt)
    return {"id": 1}


def check_user_exist(user_id: int) -> bool:
    """
    :param user_id:
    :return: True - if user exists, else False
    """
    with Session() as s:
        stmt = f'''SELECT * FROM users
                  WHERE users.id = {user_id}'''
        exists = s.execute(stmt)
    for i in exists:
        if i[0]:
            return True
    return False


def is_admin(user_id: int) -> bool:
    """
    hi
    :param user_id: ,
    :return: True - if user admin, else False
    """
    with Session() as s:
        stmt = f'''SELECT is_admin FROM users
                   WHERE users.id = {user_id}'''
        is_admin = s.execute(stmt)
    for i in is_admin:
        return i[0]


def delete_user(user_id):
    """
    Удалить пользователя (все его фото, альбомы и записи о них)
    :param user_id:
    :return:
    """
    pass


def change_user(user_id: int, full_name: str = None, email: str = None, password: str = None) -> bool:
    """
    :param user_id:
    :param full_name:
    :param email:
    :param password:
    :return:
    """
    if full_name and email and password:
        set = f'''SET full_name = '{full_name}',
                      email = '{email}',
                      password = '{password}\''''
    elif full_name and email:
        set = f'''SET full_name = '{full_name}',
                      email = '{email}\''''
    elif full_name and password:
        set = f'''SET full_name = '{full_name}',
                      password = '{password}\''''
    elif email and password:
        set = f'''SET email = '{email}',
                      password = '{password}\''''
    elif full_name:
        set = f'SET full_name = \'{full_name}\''
    elif email:
        set = f'SET email = \'{email}\''
    elif password:
        set = f'SET password = \'{password}\''
    else:
        return False

    with Session() as s:
        stmt = f'UPDATE users {set} WHERE id = {user_id}'
        s.execute(stmt)
        s.commit()
    return True


def get_albums_by_user_id(owner_id, viewer_id):
    """Получить все альбомы owner'а, которые доступны viewer'у
    :param owner_id:
    :param viewer_id:
    :return: {
                "list" : [{
                        "id": Int
                        "name": String
                       }]
            }
    """