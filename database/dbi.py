from database.db_session import Session
from database.tables.users import users
from database.tables.photos import photos
from database.tables.albums import albums
from sqlalchemy import insert
from psycopg2.errors import *
from sqlalchemy.exc import *
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
    except DatabaseError:
        return False
    finally:
        s.close()
    return True


def get_photos_by_user_id(owner_id: int, viewer_id: int) -> list[photos]:
    pass

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
    Удалить пользователя (все его фото, комментарии под фото, альбомы и записи о них)
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
    set = []
    if full_name:
        set.append(f"full_name = '{full_name}'")
    if password:
        set.append(f"password = '{password}'")
    if email:
        set.append(f"email = '{email}'")
    set = "SET " + ",\n".join(set)

    with Session() as s:
        stmt = f'UPDATE users {set} WHERE id = {user_id}'
        s.execute(stmt)
        s.commit()
    return True


def get_albums_by_user_id(owner_id: int, viewer_id: int) -> list[albums]:
    """Получить все альбомы owner'а, которые доступны viewer'у
    :param owner_id:
    :param viewer_id:
    :return: {
                "list" : [{
                        "id": Int,
                        "name": String,
                        ...
                       }]
            } or maybe just:
                [{
                    "id": Int,
                    "name": String,
                    ...
                }]
    """