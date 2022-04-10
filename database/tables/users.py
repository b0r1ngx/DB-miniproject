from sqlalchemy import Column, Integer, String, Boolean, DateTime, orm
from database.db_session import Base
from datetime import datetime as dt
from database.tables.albums import albums
# from database.tables.photos import photos
# from database.tables.comments import comments
# from database.tables.photo_access import photo_access
# from database.tables.album_access import album_access


class users(Base):
    __tablename__ = "users"

    # Table columns
    id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=dt.now())

    # Relations
    albums = orm.relation("albums", backref="users")
    photos = orm.relation("photos", backref="users")
    comments = orm.relation("comments", backref="users")
    photo_access = orm.relation("photo_access", backref="users")
    album_access = orm.relation("album_access", backref="users")
