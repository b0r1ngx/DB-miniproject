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


def select_from_users() -> list:
    with Session() as s:
        user_list = s.query(users).all()
    return user_list


if __name__ == "__main__":
    init_database_session()
    print(select_from_users())
    # print(dbi.login('perkeboring@gmail.com', 'lol'))
    # print(dbi.login('perkeboring@gmail.com', 'perkeboring'))
    # print(email_exists('perkeboring@gmail.com'))
    print(registration('Ivan Ivanov', 'ivan@gmail.com', 'mypassword'))
    # test_query()
    # print(is_admin(1))
    # print(change_user(2, full_name="IAT", email="some@mail.com", password="zxc"))
    print(select_from_users())
