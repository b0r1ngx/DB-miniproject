from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey,orm
from database.db_session import Base
from datetime import datetime as dt
from database.tables.comments import comments
from database.tables.photo_tags import photo_tags
from database.tables.photo_themes import photo_themes
from database.tables.album_photos import album_photos


class photos(Base):
    __tablename__ = "photos"

    # Table columns
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    url = Column(String)
    width = Column(Integer)
    height = Column(Integer)
    place = Column(String)  # I think there may be coordinates "63, 58", and later our service dedicate a place by coords
    description = Column(String)
    private = Column(Boolean, default=False)
    created_at = Column(DateTime, default=dt.now())

    # Relations
    comments = orm.relation("comments", backref="photos")
    photo_tags = orm.relation("photo_tags", backref="photos")
    photo_themes = orm.relation("photo_themes", backref="photos")
    album_photos = orm.relation("album_photos", backref="photos")
    photo_access = orm.relation("photo_access", backref="photos")
