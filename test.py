from database.db_session import init_database_session, Session
from database.tables.users import users
from database import dbi


def test():
    print("add user to users")
    with Session() as s:
        # s.add(users(full_name="Kirill Ivanov", email="perkeboring@gmail.com", password="perkeboring", is_admin=True))
        s.add(users(full_name="Ilya Tsaplin", email="asd@gmail.com", password="qwerty", is_admin=True))
        print("user added")
        s.commit()


def test_query():
    with Session() as s:
        user_list = s.query(users).all()
        print(user_list)


if __name__ == "__main__":
    init_database_session()
    # test_query()
    print(dbi.login('perkeboring@gmail.com', 'lol'))
    print(dbi.login('perkeboring@gmail.com', 'perkeboring'))
