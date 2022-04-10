from sqlalchemy import Column, Integer, ForeignKey
from database.db_session import Base
from database.tables.photos import photos


class photo_access(Base):
    __tablename__ = "photo_access"

    # Table columns
    id = Column(Integer, primary_key=True, autoincrement=True)
    photo_id = Column(Integer, ForeignKey("photos.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
