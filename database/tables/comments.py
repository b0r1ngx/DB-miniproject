from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, orm
from database.db_session import Base


class comments(Base):
    __tablename__ = "comments"

    # Table columns
    id = Column(Integer, primary_key=True, autoincrement=True)
    photo_id = Column(Integer, ForeignKey("photos.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    text = Column(String)
    created_at = Column(DateTime)

    # Relations
    photos = orm.relation("photos", backref="comments")
    users = orm.relation("users", backref="comments")
