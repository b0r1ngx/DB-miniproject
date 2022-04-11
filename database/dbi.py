from database.db_session import Session
from database.tables.users import users
from database.tables.photos import photos
from database.tables.albums import albums
from sqlalchemy import insert
from psycopg2.errors import *
from sqlalchemy.exc import *


def select_all_from(table) -> list:
    with Session() as s:
        user_list = s.query(table).all()
    return user_list


# def insert_into_users(full_name, email, password, is_admin=False):
#     with Session() as s:
#         # "INSERT INTO users VALUES ({full_name}, {email}, {password}, {is_admin}, {created_at});
#         stmt = (insert(users).values(full_name, email, password, is_admin))
#         s.execute(stmt)
#         s.commit()


def login(email: str, password: str) -> int:
    """ +
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
    """ +
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
    """ +
    INSERT INTO users (full_name, email, password)
    VALUES ('{full_name}', '{email}', '{password}')
    :param full_name:
    :param email:
    :param password:
    :return: True - if successfully create account, else False
    """
    s = Session()
    try:
        s.add(users(full_name=full_name, email=email, password=password))
        s.commit()
    except BaseException as e:
        return False
        # e = type(e)
        # print(e)
        # if e is type(UniqueViolation) or e is type(IntegrityError):
        #     return False
        # else:
        #     raise Exception("Something goes wrong at dbi.registration()")
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


def is_user_exist(user_id: int) -> bool:
    """ +
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
    """ +
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
    """ +
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
    pass


def is_album_name_not_exists(user_id: int, name: str) -> bool:
    """+
    :param user_id:
    :param name:
    :return:
    """
    with Session() as s:
        stmt = f'''SELECT * FROM albums
                   WHERE user_id = {user_id} 
                   AND name = '{name}\''''
        exists = s.execute(stmt)
    for i in exists:
        if i[0]:
            return False
    return True


def create_album(user_id: int, name: str, description: str) -> bool:
    """+
    Создать новый альбом
    :param user_id:
    :param name:
    :param description:
    :return:
    """
    with Session() as s:
        if is_album_name_not_exists(user_id, name):
            s.add(albums(user_id=user_id, name=name, description=description))
            s.commit()
        else:
            return False
    return True


def is_album_exist(user_id: int, album_id: int) -> bool:
    """+
    Проверить существует ли альбом
    с указанным album_id принадлежащий пользователю
    с указанным user_id
    :param user_id:
    :param album_id:
    :return:
    """
    with Session() as s:
        stmt = f'''SELECT * FROM albums
                   WHERE id = {album_id}
                   AND user_id = {user_id}'''
        album_exists = s.execute(stmt)
    for i in album_exists:
        if i[0]:
            return True
    return False


def get_album_access(user_id: int, album_id: int) -> bool:
    """+
    Имеет ли пользователь с указанным user_id
    доступ к альбому с указанным album_id
    :param user_id:
    :param album_id:
    :return:
    """
    with Session() as s:
        stmt = f'''SELECT * FROM album_access
                   WHERE album_id = {album_id}
                   AND user_id = {user_id}'''
        album_exists = s.execute(stmt)
    for i in album_exists:
        if i[0]:
            return True
    return False


def get_album(album_id):
    """

    :param album_id:
    :return:
    """
    pass


def change_album(album_id, name=None, description=None):
    """
    Изменить альбом с указанным album_id
    :param album_id:
    :param name:
    :param description:
    :return:
    """
    pass


def delete_album(album_id):
    """
    Удалить альбом (что с фото?)
    :param album_id:
    :return:
    """
    pass


def create_photo(user_id, url, description, album_list, tag_list, theme_list, is_private):
    """
    Создать фото и установить необходимые доступы
    :param user_id:
    :param description:
    :param album_list:
    :param tag_list:
    :param theme_list:
    :param is_private:
    :return:
    """
    pass


def albums_exist(album_list):
    """
    Проверить все ли альбомы из списка существуют
    :param album_list:
    :return:
    """
    pass


def tags_exist(album_list):
    """
    Проверить все ли теги из списка существуют
    :param album_list:
    :return:
    """
    pass


def themes_exist(album_list):
    """
    Проверить все ли темы из списка существуют
    :param album_list:
    :return:
    """
    pass


def get_photo(photo_id, viewer_id):
    """
    Получить фото, если есть доступ
    :param photo_id:
    :param viewer_id:
    :return:
    """
    pass


def is_photo_exist(photo_id):
    """
    Существует ли фото с указанным id
    :param photo_id:
    :return:
    """
    pass


def get_photo_access_list(photo_id):
    """
    Получить список пользователей, которым доступно фото
    :param photo_id:
    :param viewer_id:
    :return:
    """


def get_user_id_by_photo_id(photo_id):
    """
    Получить id владельца фото
    :param photo_id:
    :return:
    """
    pass


def set_photo_access_list(photo_id, user_id_list):
    """
    Установить доступ к фото пользователям
    из user_id_list
    :param photo_id:
    :param user_id_list:
    :return:
    """


def get_access_to_photo_by_user_id(photo_id, viewer_id):
    """
    Имеет ли пользователь с viewer_id досуп
    к фото с photo_id&
    :param photo_id:
    :param viewer_id:
    :return:
    """
    pass


def add_comment(commentator_id, photo_id, text):
    """
    Добавить новый комментарий к фото
    :param commentator_id:
    :param photo_id:
    :return:
    """


def get_theme_list():
    """
    Получить список существующих тем
    :return:
    """
    pass


def is_theme_exist(theme_id):
    """
    Существует ли тема с таким id
    get
    :param theme_id:
    :return:
    """
    pass


def is_tag_exist(tag_id):
    """
    Существует ли тема с таким id
    get
    :param theme_id:
    :return:
    """
    pass


def create_theme(name):
    """
    Вернуть id и название
    :param name:
    :return:
    """
    pass


def get_photos_by_theme(theme_id, viewer_id):
    """
    Получить все фото, у которых есть тема theme_id
    и которые доступны viewer_id
    :param viewer_id:
    :param theme_id:
    :return:
    """


def get_tag_list():
    """
    Получить список существующих тегов
    :return:
    """
    pass


def create_tag(name):
    """
    Вернуть id и название
    :param name:
    :return:
    """
    pass