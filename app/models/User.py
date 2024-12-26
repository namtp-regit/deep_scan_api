from sqlalchemy import Column, Integer, String
from database.base import Base


class User(Base):
    __tablename__ = "users"
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    name: str = Column(String(150), nullable=False)
    email: str = Column(String(100), unique=True, nullable=False)

    class Config:
        orm_mode = True
