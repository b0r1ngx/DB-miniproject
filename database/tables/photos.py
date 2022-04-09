from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey,orm
from database.db_session import Base


class photos(Base):
    __tablename__ = "photos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    url = Column(String)
    width = Column(Integer)
    height = Column(Integer)
    place = Column(String)  # I think there may be coordinates "63, 58", and later our service dedicate a place by coords
    description = Column(String)
    private = Column(Boolean, default=False)
    created_at = Column(DateTime)

    comments = orm.relation("comments", back_populates="photos")
    albums = orm.relation("albums", back_populates="photos")
    users = orm.relation("users")
