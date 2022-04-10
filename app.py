import datetime

from database.db_session import init_database_session, Session
from database.tables.users import users
from main import app


def test():
    print("add user to users")
    with Session() as s:
        s.add(users(full_name="Kirill Ivanov", email="perkeboring@gmail.com", password="perkeboring",
                    is_admin=True, created_at=datetime.date(2015, 4, 12)))
        s.commit()


def test_query():
    with Session() as s:
        print("SELECT * FROM users", s.query(users).all())


if __name__ == "__main__":
    init_database_session()
    test()
    test_query()

