from sqlalchemy import Column, Integer, ForeignKey, orm
from database.db_session import Base


class photo_tags(Base):
    __tablename__ = "photo_tags"

    # Table columns
    id = Column(Integer, primary_key=True, autoincrement=True)
    photo_id = Column(Integer, ForeignKey("photos.id"))
    tag_id = Column(Integer, ForeignKey("tags.id"))
