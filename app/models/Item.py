from sqlalchemy import Column, Integer, String
from database.base import Base


class User(Base):
    __tablename__ = "items"
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    name: str = Column(String(250), nullable=False)
