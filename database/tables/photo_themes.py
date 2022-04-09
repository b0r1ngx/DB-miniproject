from sqlalchemy import Column, Integer, ForeignKey, orm
from database.db_session import Base


class photo_themes(Base):
    __tablename__ = "photo_themes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    photo_id = Column(Integer)
    theme_id = Column(Integer)