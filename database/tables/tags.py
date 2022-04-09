from sqlalchemy import Column, Integer, String
from database.db_session import Base


class tags(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True)