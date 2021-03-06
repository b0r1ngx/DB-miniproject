from sqlalchemy import Column, Integer, String, orm
from database.db_session import Base


class themes(Base):
    __tablename__ = "themes"

    # Table columns
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True)

    # Relations
    photo_themes = orm.relation("photo_themes", backref="themes")

    def __str__(self):
        return f"Theme <id: {self.id}, name: {self.name}>"

    def __repr__(self):
        return self.__str__()