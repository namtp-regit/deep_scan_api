from sqlalchemy import Column, Integer, String
from app.database.connect import Base

class User(Base):
    __tablename__ = 'users'
    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String(150), nullable=False)
    email: str = Column(String(100), unique=True, nullable=False)
