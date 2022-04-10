from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import QueuePool
from sqlalchemy import create_engine


Base = declarative_base()
Session: Session


def init_database_session():
    # How to read engine URL: dialect+driver://username:password@host:port/database
    engine = create_engine(url='postgresql+psycopg2://postgres:postgres@localhost:5432/database/db',
                           echo=False, pool_size=10, max_overflow=0, poolclass=QueuePool, pool_pre_ping=True)

    print('Подключение к базе данных')
    global Session
    Session = sessionmaker(bind=engine)

    if not database_exists(engine.url):
        print('Создание базы данных')
        create_database(engine.url)

    print('Инициализация таблиц')
    Base.metadata.create_all(engine)

    print('Объект Session, для доступа к базе данных, доступен')
