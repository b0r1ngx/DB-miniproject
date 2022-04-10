from sqlalchemy import Column, Integer, ForeignKey
from database.db_session import Base


class album_photos(Base):
    __tablename__ = "album_photos"

    # Table columns
    id = Column(Integer, primary_key=True, autoincrement=True)
    album_id = Column(Integer, ForeignKey("albums.id"))
    photo_id = Column(Integer, ForeignKey("photos.id"))
