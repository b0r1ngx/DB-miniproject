from sqlalchemy import Column, Integer, String, orm
from database.db_session import Base


class tags(Base):
    __tablename__ = "tags"

    # Table columns
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True)

    # Relations
    photo_tags = orm.relation("photo_tags", backref="tags")