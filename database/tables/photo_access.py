from sqlalchemy import Column, Integer, ForeignKey, orm
from database.db_session import Base


class photo_access(Base):
    __tablename__ = "photo_access"

    # Table columns
    id = Column(Integer, primary_key=True, autoincrement=True)
    photo_id = Column(Integer, ForeignKey("photos.id"))
    user_id = Column(Integer, ForeignKey("users.id"))

    # Relations
    photos = orm.relation("photos", backref="photo_access")
    users = orm.relation("users", backref="photo_access")
