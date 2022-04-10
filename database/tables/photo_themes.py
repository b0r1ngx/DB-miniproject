from sqlalchemy import Column, Integer, ForeignKey, orm
from database.db_session import Base


class photo_themes(Base):
    __tablename__ = "photo_themes"

    # Table columns
    id = Column(Integer, primary_key=True, autoincrement=True)
    photo_id = Column(Integer, ForeignKey("photos.id"))
    theme_id = Column(Integer, ForeignKey("themes.id"))
