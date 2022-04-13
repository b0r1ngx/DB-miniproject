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
from database.dbi import *
from generator import *

from time import time


def test_query(owner_id: int, viewer_id: int) -> None:
    with Session() as s:
        private = s.query(photos).filter(
            photos.private == True,
            photos.user_id == owner_id
        )
        user_access = s.query(photo_access).filter(
            photo_access.user_id == viewer_id
        )

        private_with_acc = private.join(user_access)
        private_list = private_with_acc.all()


if __name__ == '__main__':
    init_database_session()
    user_list = select_all_from(users)
    photo_list = select_all_from(photos)
    print(len(user_list))
    print(len(photo_list))
    owner_id = 3
    viewer_id = 4
    print("Генерирую данные")
    # generate_photos(user_id=owner_id)
    generate_photo_access(user_id=viewer_id)
    generate_comments(amount=1000, photo_id=500)
    # print("DATA SIZE:", len(select_all_from(photos)))

    time_list = []
    print("Начинаю делать запросы")
    for i in range(15):
        t = time()
        # get_photo(500, viewer_id)
        get_users_photos(owner_id, viewer_id)
        # test_query(2, 3)
        t1 = time()
        time_list.append(t1 - t)
    print('All times', time_list)
    print('AVG time', sum(time_list) / len(time_list))
