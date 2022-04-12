from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, orm
from database.db_session import Base
from datetime import datetime as dt
from database.tables.photo_access import photo_access
from database.tables.album_access import album_access


class albums(Base):
    __tablename__ = "albums"

    # Table columns
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String)
    description = Column(String)
    created_at = Column(DateTime, default=dt.now())

    # Relations
    album_photos = orm.relation("album_photos", backref="albums")
    album_access = orm.relation("album_access", backref="albums")

    def __str__(self):
        return f"<Album ({self.id}) by user_id {self.user_id} with name: {self.name} >"

    def __repr__(self):
        return self.__str__()

    # def __dict__(self):
    #     return {
    #         "id": self.id,
    #         "user_id": self.user_id,
    #         "name": self.name,
    #         "description": self.description,
    #         "created_at": self.created_at
    #     }
