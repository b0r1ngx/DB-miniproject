from sqlalchemy import Column, Integer, String, Boolean, DateTime, orm
from database.db_session import Base


class users(Base):
    __tablename__ = "users"

    # Table columns
    id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    is_admin = Column(Boolean)
    created_at = Column(DateTime)

    # Relations
    albums = orm.relation("albums", backref="users")
    photos = orm.relation("photos", backref="users")
    comments = orm.relation("comments", backref="users")
    photo_access = orm.relation("photo_access", backref="users")
    album_access = orm.relation("album_access", backref="users")
