from sqlalchemy import Column, Integer, ForeignKey, orm
from database.db_session import Base


class album_photos(Base):
    __tablename__ = "album_photos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    album_id = Column(Integer)
    user_id = Column(Integer)