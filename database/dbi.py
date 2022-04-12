from database.db_session import Session
from database.tables.users import users
from database.tables.photos import photos
from database.tables.albums import albums
from database.tables.themes import themes
from database.tables.tags import tags
from database.tables.themes import themes
from database.tables.photo_tags import photo_tags
from database.tables.album_access import album_access
from database.tables.album_photos import album_photos
from database.tables.photo_themes import photo_themes
from database.tables.photo_access import photo_access
from database.tables.comments import comments

from sqlalchemy import insert
from psycopg2.errors import *
from sqlalchemy.exc import *


def select_all_from(table) -> list:
    with Session() as s:
        table_list = s.query(table).all()
    # with session as s:
    #     user_list = s.query(table).all()
    return table_list


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


def create_album(user_id: int, name: str, description: str):
    """+
    Создать новый альбом
    :param user_id:
    :param name:
    :param description:
    :return: dict or None
    """
    with Session() as s:
        if is_album_name_not_exists(user_id, name):
            new_album = albums(user_id=user_id, name=name, description=description)
            s.add(new_album)
            s.commit()
            new_album = {
                "id": new_album.id,
                "name": new_album.name,
            }
            return new_album
    return None


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
    set = []
    if name:
        set.append(f"name = '{name}'")
    if description:
        set.append(f"description = '{description}'")
    set = "SET " + ",\n".join(set)

    with Session() as s:
        stmt = f'UPDATE albums {set} WHERE id = {album_id}'
        s.execute(stmt)
        s.commit()
    return True


def delete_album(album_id):
    """
    Удалить альбом (что с фото?)
    Удалить альбом + все записи о нем в других таблицах (с ним в album_access)
    :param album_id:
    :return:
    """
    pass


def create_photo(user_id: int, url: str, description: str, album_list: list[int],
                 tag_list: list[int], theme_list: list[int], is_private) -> dict:
    """+
    Создать фото и установить необходимые доступы
    :param url:
    :param user_id:
    :param description:
    :param album_list:
    :param tag_list:
    :param theme_list:
    :param is_private:
    :return: dict or None
    """
    with Session() as s:
        new_photo = photos(user_id=user_id,
                           url=url,
                           description=description,
                           private=is_private)
        s.add(new_photo)

        s.add(photo_themes())
        s.commit()
        new_photo_id = new_photo.id
        new_photo_url = new_photo.url
        if theme_list:
            for theme_id in theme_list:
                s.add(photo_themes(photo_id=new_photo_id,
                                   theme_id=theme_id))
        if tag_list:
            for tag_id in tag_list:
                s.add(photo_tags(photo_id=new_photo_id,
                                 tag_id=tag_id))
        if album_list:
            for album_id in album_list:
                s.add(album_photos(photo_id=new_photo_id,
                                   album_id=album_id))
        s.commit()  # TODO Проверить хорошо ли добавляет
        return {
            "id": new_photo_id,
            "url": new_photo_url
        }


def albums_exist(album_list: list[int]) -> bool:
    """+
    Проверить все ли альбомы из списка существуют
    :param album_list:
    :return:
    """
    size = len(album_list)
    if size == 1:
        condition = f"({album_list[0]})"
    else:
        album_list = tuple(album_list)
        condition = f"{album_list}"

    with Session() as s:
        stmt = f'''SELECT count(*) from albums
                   WHERE id IN {condition}'''
        count = s.execute(stmt)
    for i in count:
        if i[0] != size:
            return False
    return True


def tags_exist(tag_list: list[int]) -> bool:
    """+
    Проверить все ли теги из списка существуют
    :param tag_list:
    :return:
    """
    size = len(tag_list)
    if size == 1:
        condition = f"({tag_list[0]})"
    else:
        tag_list = tuple(tag_list)
        condition = f"{tag_list}"

    with Session() as s:
        stmt = f'''SELECT count(*) from tags
                   WHERE id IN {condition}'''
        count = s.execute(stmt)
    for i in count:
        if i[0] != size:
            return False
    return True


def themes_exist(theme_list: list[int]) -> bool:
    """+
    Проверить все ли темы из списка существуют
    :param theme_list:
    :return:
    """
    size = len(theme_list)
    if size == 1:
        condition = f"({theme_list[0]})"
    else:
        theme_list = tuple(theme_list)
        condition = f"{theme_list}"

    with Session() as s:
        stmt = f'''SELECT count(*) FROM themes
                   WHERE id IN {condition}'''
        count = s.execute(stmt)
    for i in count:
        if i[0] != size:
            return False
    return True


def get_photo(photo_id: int, viewer_id: int):
    """
    Получить фото, если есть доступ
    :param photo_id:
    :param viewer_id:
    :return:
    """
    with Session() as s:
        stmt = f'''SELECT * FROM photos
                   LEFT JOIN photo_access pa USING ()'''


def is_photo_exist(photo_id):
    """+
    Существует ли фото с указанным id
    :param photo_id:
    :return:
    """
    with Session() as s:
        rows = s.query(photos).filter(photos.id == photo_id).all()
        if len(rows) > 0:
            return True
        return False


def get_photo_access_list(photo_id):
    """+
    Получить список пользователей, которым доступно фото
    :param photo_id:
    :param viewer_id:
    :return:
    """
    with Session() as s:
        rows = s.query(photo_access).filter(photo_access.photo_id == photo_id).all()
        result_list = []
        for row in rows:
            result_list.append(row.user_id)
        return result_list
    pass


def get_user_id_by_photo_id(photo_id):
    """+
    Получить id владельца фото
    :param photo_id:
    :return:
    """
    with Session() as s:
        photo = s.query(photos).filter(photos.id == photo_id).one()
        user_id = photo.user_id
        return user_id


def get_access_to_photo_by_user_id(photo_id, viewer_id):
    """+
    Имеет ли пользователь с viewer_id досуп
    к фото с photo_id&
    :param photo_id:
    :param viewer_id:
    :return:
    """
    with Session() as s:
        photo = s.query(photos).filter(photos.id == photo_id).one()
        photo_is_private = photo.private
        if not photo_is_private:
            return True
        if viewer_id in get_photo_access_list(photo_id):
            return True
        if viewer_id == get_user_id_by_photo_id(photo_id):
            return True
        return False
        # #  TODO realize add access and resume
        # print(some)

        # public_images = s.query(photos).filter(photos.private == False).all()
        # some1
        # # some = some.join
        # print(photo)
    pass


def add_comment(commentator_id, photo_id, text):
    """+
    Добавить новый комментарий к фото
    :param commentator_id:
    :param photo_id:
    :return:
    """
    with Session() as s:
        new_comment = comments(text=text,
                               user_id=commentator_id,
                               photo_id=photo_id)
        s.add(new_comment)
        s.commit()
        return {
            "id": new_comment.id,
            "user": new_comment.user_id,
            "photo_id": new_comment.photo_id,
            "text": new_comment.text
        }


def get_theme_list() -> list[themes]:
    """
    Получить список существующих тем
    :return:
    """
    return select_all_from(themes)


def is_theme_exist(theme_id: int) -> bool:
    """
    Существует ли тема с таким id
    get
    :param theme_id:
    :return:
    """
    with Session() as s:
        stmt = f'''SELECT * FROM themes
                   WHERE id = {theme_id}'''
        theme_exist = s.execute(stmt)
    for i in theme_exist:
        if i[0]:
            return True
    return False


def is_tag_exist(tag_id: int) -> bool:
    """
    Существует ли тема с таким id
    get
    :param tag_id:
    :return:
    """
    with Session() as s:
        stmt = f'''SELECT * FROM tags
                    WHERE id = {tag_id}'''
        tag_exist = s.execute(stmt)
    for i in tag_exist:
        if i[0]:
            return True
    return False


def create_theme(name):
    """+
    Вернуть id и название
    :param name:
    :return: dict or None
    """
    try:
        with Session() as s:
            new_theme = themes(name=name)
            s.add(new_theme)
            s.commit()
            return {
                "id": new_theme.id,
                "name": new_theme.name
            }
    except IntegrityError:
        print("Такая тема уже существует")
    return None


def get_photos_by_tag(tag_id, viewer_id):
    """
    Получить все фото, у которых есть тег tag_id
    и которые доступны viewer_id
    :param tag_id:
    :param viewer_id:
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
    with Session() as s:
        return select_all_from(tags)


def create_tag(name):
    """+
    Вернуть id и название
    :param name:
    :return: dict or None
    """
    try:
        with Session() as s:
            new_tag = tags(name=name)
            s.add(new_tag)
            s.commit()
            return {
                "id": new_tag.id,
                "name": new_tag.name
            }
    except IntegrityError:
        print("Такой тег уже существует")
    return None


def add_user_to_photo_access(photo_id, accesser_id):
    """+
    добавить пользователя в список доступа и вернуть ид новой записи
    если уже там, то не добавлять, а вернуть ид старой записи
    :param photo_id:
    :param accesser_id:
    :return:
    """
    with Session() as s:
        rows = s.query(photo_access).filter(
            photo_access.photo_id == photo_id,
            photo_access.user_id == accesser_id
        ).all()

        if len(rows) == 0:
            new_photo_access = photo_access(
                photo_id=photo_id,
                user_id=accesser_id
            )
            s.add(new_photo_access)
            s.commit()
            new_photo_access_id = new_photo_access.id
            return new_photo_access_id

        return rows[0].id


def delete_user_to_photo_access(photo_id, accesser_id):
    """+
    Удалить пользователя если был
    :param photo_id:
    :param accesser_id:
    :return: True - success
    """
    with Session() as s:
        rows = s.query(photo_access).filter(
            photo_access.user_id == accesser_id,
            photo_access.photo_id == photo_id
        ).all()
        if len(rows) > 0:
            s.delete(rows[0])
        s.commit()
        return True
