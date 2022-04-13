from database.db_session import init_database_session, Session
from database.tables.users import users
from database.dbi import *


def insert_into_users():
    print("add user to users")
    with Session() as s:
        # s.add(users(full_name="Kirill Ivanov", email="perkeboring@gmail.com", password="perkeboring", is_admin=True))
        s.add(users(full_name="Ilya Tsaplin", email="asd@gmail.com", password="qwerty", is_admin=True))
        print("user added")
        s.commit()


if __name__ == "__main__":
    init_database_session()
    # print(select_all_from(users))
    # print(dbi.login('perkeboring@gmail.com', 'lol'))
    # print(dbi.login('perkeboring@gmail.com', 'perkeboring'))
    # print(email_exists('perkeboring@gmail.com'))
    # print(registration('Ivan Ivanov', 'ivank@gmail.com', 'mypassword'))
    # print(is_album_name_not_exists(1, 'Best Album'))
    # print(create_album(1, 'Best Album', ';]'))
    # print(is_album_name_not_exists(1, 'Best Album'))
    # print(select_all_from(albums))
    # print(check_album_exist(1, 1))
    # print(get_album_access(1, 1))
    # test_query()
    # print(is_admin(13))
    # print(change_user(2, full_name="IAT", email="some@mail.com", password="zxc"))
    # print(type(select_all_from(users)))
    # print(select_all_from(albums))
    # print(get_tag_list())
    # print(type(create_tag("qwerty11")))
    # print(get_tag_list())
    # print(albums_exist([1]))
    # print(registration("Privet", "a@a@mail.ru", "priveta"))

    # print(delete_user(1))
    # print(get_users_photos(1, 3))
    # print(delete_photo(2769))
    # print(get_users_photos(1, 3))

    # with Session() as s:
    #     photo_theme = s.query(photo_themes).filter(photo_themes.photo_id == 183).all()
    #
    # print(photo_theme)

    # while True:
    #     print("------themes----------------------------------------")
    #     my_list = select_all_from(themes)
    #     for row in my_list:
    #         print(row)
    #     print("------tags----------------------------------------")
    #     my_list = select_all_from(tags)
    #     for row in my_list:
    #         print(row)
    #     print("------albums----------------------------------------")
    #     my_list = select_all_from(albums)
    #     for row in my_list:
    #         print(row)
    #     print("------photos----------------------------------------")
    #     my_list = select_all_from(photos)
    #     for row in my_list:
    #         print(row)
    #     print("------users----------------------------------------")
    #     my_list = select_all_from(users)
    #     for row in my_list:
    #         print(row)
    #     print("------users----------------------------------------")
    #     my_list = select_all_from(users)
    #     for row in my_list:
    #         print(row)
    #
    #     check_album_list_owner(2, [1, 2, 4, 5])
    #
    #     print(get_users_photos(2, 9))
    #     input("press Enter")
    # print(select_all_from(users))
    # print(select_all_from(photos))
    # print(select_all_from(photo_access))
    # with Session() as s:
    #     photo_theme = s.query(photo_access).filter(photo_access.photo_id == 1).all()
    #
    # print(photo_theme)
    # print(get_photo(1, 79))
    # print(get_photo(1, 100))
    # print(get_photo(1, 86))

    print(photo_theme)
    print(get_photo(1, 79))
    print(get_photo(1, 100))
    print(get_photo(1, 86))

    email = 'perkeboring@gmail.com'
    print(registration('Kirill Ivanov', email, 'privetiki3'))
    print(login(email, 'privetiki3'))
    with Session() as s:
        user = s.query(users).filter(users.email == email)
    print(user.first().password)
    # print(get_user_info(3))

    print(get_photos_by_theme(4))


