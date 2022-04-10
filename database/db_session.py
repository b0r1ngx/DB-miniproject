from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import QueuePool
from sqlalchemy import create_engine
from constants import db

Base = declarative_base()
Session: Session = sessionmaker()


def init_database_session():
    engine = create_engine(url=db, echo=False, pool_size=10, max_overflow=0, poolclass=QueuePool, pool_pre_ping=True)

    print('Подключение к базе данных')
    Session.configure(bind=engine)

    if not database_exists(engine.url):
        print('Создание базы данных')
        create_database(engine.url)

    print('Инициализация таблиц')
    Base.metadata.create_all(engine)

    print('Объект Session, для доступа к базе данных, доступен')
