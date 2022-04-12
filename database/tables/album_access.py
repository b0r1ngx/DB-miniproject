from sqlalchemy import Column, Integer, ForeignKey
from database.db_session import Base


class album_access(Base):
    __tablename__ = "album_access"

    # Table columns
    id = Column(Integer, primary_key=True, autoincrement=True)
    album_id = Column(Integer, ForeignKey("albums.id", ondelete="CASCADE"))
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
