from sqlalchemy import Column, Integer, ForeignKey
from database.db_session import Base
from database.tables.themes import themes


class photo_themes(Base):
    __tablename__ = "photo_themes"

    # Table columns
    id = Column(Integer, primary_key=True, autoincrement=True)
    photo_id = Column(Integer, ForeignKey("photos.id", ondelete="CASCADE"))
    theme_id = Column(Integer, ForeignKey("themes.id", ondelete="CASCADE"))

    def __str__(self):
        return f"theme_to_photo:\t<id: {self.id},\ttheme_id:{self.theme_id},\tphoto_id: {self.photo_id}>"

    def __repr__(self):
        return self.__str__()
