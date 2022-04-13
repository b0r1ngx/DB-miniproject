import random

from database.db_session import init_database_session, Session
from database.dbi import select_all_from
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

from string import ascii_lowercase, digits
from random import choice, choices, randint


def random_seq(size=10, chars=ascii_lowercase + digits) -> str:
    return ''.join(choices(chars, k=randint(3, size)))


def random_user(full_name_chars='', email_chars='', pass_chars='') -> dict:
    full_name = random_seq() + ' ' + random_seq()
    email = random_seq(15) + '@gmail.com'
    password = random_seq(32)
    return {
        'full_name': full_name,
        'email': email,
        'password': password
    }


def generate_users(amount: int = 100) -> None:
    """Users are looked like aliens ~^-^~ sorry for that
    :param amount:
    :return:
    """
    if amount <= 0:
        return

    user_list: list[dict] = []
    for i in range(amount):
        user_list.append(random_user())

    user_list = list(map(lambda u: users(**u), user_list))
    with Session() as s:
        s.bulk_save_objects(user_list)
        s.commit()


def generate_themes(t: list = None) -> None:
    """Generate themes that are given in t
    :param t:
    :return:
    """
    if t is None:
        t = ['Nature', 'Ocean', 'Mountains', 'Fire', 'Sky', 'Space', 'City', 'Animals']

    theme_list: list[dict] = []
    for th in t:
        theme = {
            'name': th
        }
        theme_list.append(theme)

    theme_list = list(map(lambda t: themes(**t), theme_list))
    with Session() as s:
        s.bulk_save_objects(theme_list)
        s.commit()


def generate_tags(t: list = None) -> None:
    """Generate tags that are given in t
    :param t:
    :return:
    """
    if t is None:
        t = ['#Nature', '#Ocean', '#Mountains', '#Fire', '#Sky', '#Space', '#City', '#Animals',
             '#cool', '#wow', '#lol', '#awesome', '#super', '#ilovelife', '#wealltogether', '#flowers']

    tag_list: list[dict] = []
    for tg in t:
        tag = {
            'name': tg
        }
        tag_list.append(tag)

    tag_list = list(map(lambda t: tags(**t), tag_list))
    with Session() as s:
        s.bulk_save_objects(tag_list)
        s.commit()


def generate_photos(amount: int = 10000) -> None:
    if amount <= 0:
        return

    # Determine how users we have, to later append to this info a photos
    with Session() as s:
        user_list = s.query(users).all()
    amount_of_users = len(user_list)

    photo_list: list[dict] = []
    for i in range(amount):
        photo = {
            'user_id': randint(1, amount_of_users),
            'url': '/upload/' + random_seq(64) + '.png',
            'description': random_seq(100),
            'private': choice([False, False, True])
        }
        photo_list.append(photo)

    photo_list = list(map(lambda p: photos(**p), photo_list))
    with Session() as s:
        s.bulk_save_objects(photo_list)
        s.commit()


def generate_photo_to_themes() -> None:
    # get themes 'n photos
    with Session() as s:
        theme_list = s.query(themes).all()
        photo_list = s.query(photos).all()

        # associate it in table
        photo_to_themes_list: list[dict] = []
        for photo in photo_list:
            ptt = {
                'photo_id': photo.id,
                'theme_id': choice(theme_list).id
            }
            photo_to_themes_list.append(ptt)

        photo_to_themes_list = list(map(lambda ptt: photo_themes(**ptt), photo_to_themes_list))
        s.bulk_save_objects(photo_to_themes_list)
        s.commit()


def generate_photo_to_tags() -> None:
    # get tags 'n photos
    with Session() as s:
        tag_list = s.query(tags).all()
        photo_list = s.query(photos).all()

        # associate it in table
        photo_to_tags_list: list[dict] = []
        for photo in photo_list:
            ptt = {
                'photo_id': photo.id,
                'tag_id': choice(tag_list).id
            }
            photo_to_tags_list.append(ptt)

        photo_to_tags_list = list(map(lambda ptt: photo_tags(**ptt), photo_to_tags_list))
        s.bulk_save_objects(photo_to_tags_list)
        s.commit()


def generate_photo_access() -> None:
    # get users 'n photos
    with Session() as s:
        user_list = s.query(users).all()
        photo_list = s.query(photos).all()

        # associate it in table
        photo_access_list: list[dict] = []
        for photo in photo_list:
            # just simple, may generate access to user that own this photo
            pa = {
                'photo_id': photo.id,
                'user_id': choice(user_list).id
            }
            photo_access_list.append(pa)

        photo_access_list = list(map(lambda pa: photo_access(**pa), photo_access_list))
        s.bulk_save_objects(photo_access_list)
        s.commit()


def generate_comments(amount: int = 100, max_comments_per_photo: int = 10) -> None:
    """Also users is messaging at some alien language ~._.~
    :param max_comments_per_photo:
    :param amount:
    :return:
    """
    if amount <= 0:
        return

    # need to get users 'n photos
    with Session() as s:
        user_list = s.query(users).all()
        photo_list = s.query(photos).all()

    comment_list: list[dict] = []
    for photo in photo_list:
        for i in range(randint(1, max_comments_per_photo)):
            comment = {
                'photo_id': photo.id,
                'user_id': choice(user_list).id,
                'text': random_seq(100)
            }
            comment_list.append(comment)

    comment_list = list(map(lambda c: comments(**c), comment_list))
    with Session() as s:
        s.bulk_save_objects(comment_list)
        s.commit()


def generate_albums(max_albums: int = 5) -> None:
    """Alien language everywhere ;c
    :param max_albums:
    :param amount:
    :return:
    """
    # need to get users
    with Session() as s:
        user_list = s.query(users).all()

    album_list: list[dict] = []
    for user in user_list:
        for i in range(randint(1, max_albums)):
            album = {
                'user_id': user.id,
                'name': random_seq(32),
                'description': random_seq(255)
            }
            album_list.append(album)

    album_list = list(map(lambda a: albums(**a), album_list))
    with Session() as s:
        s.bulk_save_objects(album_list)
        s.commit()


def generate_album_photos() -> None:
    """Filling user albums with users photos
    :return:
    """
    # need to get albums 'n photos that user can append to album (only his photos)
    with Session() as s:
        album_list = s.query(albums).all()

    album_photo_list: list[dict] = []
    for album in album_list:
        photo_list = s.query(photos).filter(photos.user_id == album.id).all()
        if len(photo_list) <= 1:
            continue
        for i in range(randint(2, len(photo_list))):
            album_photo = {
                'photo_id': choice(photo_list).id,
                'album_id': album.id
            }
            album_photo_list.append(album_photo)

    album_photo_list = list(map(lambda ap: album_photos(**ap), album_photo_list))
    with Session() as s:
        s.bulk_save_objects(album_photo_list)
        s.commit()


def generate_album_access() -> None:
    # get users 'n albums
    with Session() as s:
        user_list = s.query(users).all()
        album_list = s.query(albums).all()

        # associate it in table
        album_access_list: list[dict] = []
        for album in album_list:
            # just simple, may generate access to user that own this album
            pa = {
                'album_id': album.id,
                'user_id': choice(user_list).id
            }
            album_access_list.append(pa)

        album_access_list = list(map(lambda aa: album_access(**aa), album_access_list))
        s.bulk_save_objects(album_access_list)
        s.commit()


if __name__ == "__main__":
    init_database_session()

    # after you generate one time, comment these lines please, if you wanna just look at prints
    print("Генерирую данные:")
    generate_users()
    generate_themes()
    generate_tags()
    generate_photos()
    generate_photo_to_themes()
    generate_photo_to_tags()
    generate_photo_access()
    generate_comments()
    generate_albums()
    generate_album_photos()
    generate_album_access()

    print("Вывожу данные:")
    print(select_all_from(users))
    print(select_all_from(themes))
    print(select_all_from(tags))
    print(select_all_from(photos))
    print(select_all_from(photo_themes))
    print(select_all_from(photo_tags))
    print(select_all_from(photo_access))
    print(select_all_from(comments))
    print(select_all_from(albums))
    print(select_all_from(album_photos))
    print(select_all_from(album_access))
