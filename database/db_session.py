from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
from sqlalchemy import create_engine


Base = declarative_base()

path = 'database/db'
engine = create_engine(url='postgresql+psycopg2://@localhost/' + path,
                       echo=False, pool_size=10, max_overflow=0, poolclass=QueuePool, pool_pre_ping=True)

print('Подключение к базе данных')
session = sessionmaker(bind=engine)

print('Инициализация таблиц')
Base.metadata.create_all(engine)