from sqlalchemy import Column, Integer, ForeignKey
from database.db_session import Base
from database.tables.tags import tags


class photo_tags(Base):
    __tablename__ = "photo_tags"

    # Table columns
    id = Column(Integer, primary_key=True, autoincrement=True)
    photo_id = Column(Integer, ForeignKey("photos.id", ondelete="CASCADE"))
    tag_id = Column(Integer, ForeignKey("tags.id", ondelete="CASCADE"))

    def __str__(self):
        return f"tag_to_photo:\t<id: {self.id},\ttag_id:{self.tag_id},\tphoto_id: {self.photo_id}>"

    def __repr__(self):
        return self.__str__()
