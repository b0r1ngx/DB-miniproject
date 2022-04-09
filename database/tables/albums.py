from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, orm
from database.db_session import Base


class albums(Base):
    __tablename__ = "albums"

    # Table columns
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String)
    description = Column(String)
    created_at = Column(DateTime)

    # Relations
    users = orm.relation("users", backref="albums")
    album_photos = orm.relation("album_photos", backref="albums")
    album_access = orm.relation("album_access", backref="albums")
