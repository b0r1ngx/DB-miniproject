from sqlalchemy import Column, Integer, ForeignKey, orm
from database.db_session import Base


class album_photos(Base):
    __tablename__ = "album_photos"

    # Table columns
    id = Column(Integer, primary_key=True, autoincrement=True)
    album_id = Column(Integer, ForeignKey("albums.id"))
    photo_id = Column(Integer, ForeignKey("photos.id"))

    # Relations
    albums = orm.relation("albums", backref="album_photos")
    photos = orm.relation("photos", backref="album_photos")
