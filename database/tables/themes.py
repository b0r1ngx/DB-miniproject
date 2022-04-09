from sqlalchemy import Column, Integer, String
from database.db_session import Base


class themes(Base):
    __tablename__ = "themes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True)