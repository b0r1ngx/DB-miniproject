from sqlalchemy import Column, Integer, String, DateTime, orm
from database.db_session import Base


class users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    created_at = Column(DateTime)

    comments = orm.relation("comments", back_populates="users")
    albums = orm.relation("albums", back_populates="photos")