from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from database.db_session import Base
from datetime import datetime as dt


class comments(Base):
    __tablename__ = "comments"

    # Table columns
    id = Column(Integer, primary_key=True, autoincrement=True)
    photo_id = Column(Integer, ForeignKey("photos.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    text = Column(String)
    created_at = Column(DateTime, default=dt.now())
