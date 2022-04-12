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
from random import choices, randint


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
    if amount <= 0:
        return
    user_list: list[dict] = []
    for i in range(amount):
        user_list.append(random_user())

    user_list = list(map(lambda u: users(**u), user_list))
    with Session() as s:
        s.bulk_save_objects(user_list)
        s.commit()


if __name__ == "__main__":
    init_database_session()
    generate_users(0)
    print(select_all_from(users))