from sqlalchemy import Column, Integer, ForeignKey
from database.db_session import Base
from database.tables.photos import photos


class photo_access(Base):
    __tablename__ = "photo_access"

    # Table columns
    id = Column(Integer, primary_key=True, autoincrement=True)
    photo_id = Column(Integer, ForeignKey("photos.id"))
    user_id = Column(Integer, ForeignKey("users.id"))

    def __str__(self):
        return f"Photo_access:<id: {self.id},\tphoto_id: {self.photo_id},\tuser_id: {self.user_id}>"

    def __repr__(self):
        return self.__str__()