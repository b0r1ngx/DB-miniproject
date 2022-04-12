from sqlalchemy import Column, Integer, String, orm
from database.db_session import Base


class tags(Base):
    __tablename__ = "tags"

    # Table columns
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True)

    # Relations
    photo_tags = orm.relation("photo_tags", backref="tags")

    def __str__(self):
        return f"Tag <id: {self.id}, name: {self.name}>"

    def __repr__(self):
        return self.__str__()