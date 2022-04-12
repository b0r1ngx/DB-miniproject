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
    if amount <= 0:
        return

    theme_list: list[dict] = []
    for th in range(t):
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
    if amount <= 0:
        return

    tag_list: list[dict] = []
    for tg in range(t):
        tag = {
            'name': tg
        }
        tag_list.append(tag)

    tag_list = list(map(lambda t: tags(**t), tag_list))
    with Session() as s:
        s.bulk_save_objects(tag_list)
        s.commit()


def generate_photos(amount: int = 100) -> None:
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
            'url': '/upload/' + random_seq(32) + '.png',
            'description': random_seq(100),
            'private': choice([False, False, True])
        }
        photo_list.append(photo)

    photo_list = list(map(lambda p: photos(**p), photo_list))
    with Session() as s:
        s.bulk_save_objects(photo_list)
        s.commit()


def generate_photo_to_themes() -> None:
    pass


def generate_photo_to_tags() -> None:
    pass


def generate_albums(amount: int = 100) -> None:
    if amount <= 0:
        return

    album_list: list[dict] = []
    for i in range(amount):
        album = {
            ''
        }
        album_list.append(album)

    album_list = list(map(lambda a: albums(**a), album_list))
    with Session() as s:
        s.bulk_save_objects(album_list)
        s.commit()


if __name__ == "__main__":
    init_database_session()
    # generate_users()
    generate_photos()
    print(select_all_from(users))
