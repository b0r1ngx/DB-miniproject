from sqlalchemy import Column, Integer, ForeignKey, orm
from database.db_session import Base


class photo_access(Base):
    __tablename__ = "photo_access"

    id = Column(Integer, primary_key=True, autoincrement=True)
    photo_id = Column(Integer)
    user_id = Column(Integer)
