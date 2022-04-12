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

    while True:
        my_list = select_all_from(photo_access)
        for row in my_list:
            print(row)
        delete_user_to_photo_access(7, None)
        input("press Enter")
    # add_user_to_photo_access(7, 8)
    # my_list = select_all_from(photo_access)
    # for row in my_list:
    #     print(row)
    # delete_user_to_photo_access(7, 8)
    # print("-----------------")
    # my_list = select_all_from(photo_access)
    # for row in my_list:
    #     print(row)

