from sqlalchemy import Column, Integer, ForeignKey
from database.db_session import Base


class album_photos(Base):
    __tablename__ = "album_photos"

    # Table columns
    id = Column(Integer, primary_key=True, autoincrement=True)
    album_id = Column(Integer, ForeignKey("albums.id"))
    photo_id = Column(Integer, ForeignKey("photos.id"))

    def __str__(self):
        return f"album_to_photo:\t<id: {self.id},\talbum_id:{self.album_id},\tphoto_id: {self.photo_id}>"

    def __repr__(self):
        return self.__str__()
