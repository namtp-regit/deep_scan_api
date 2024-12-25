from sqlalchemy import CheckConstraint, Column, Integer, String
from database.base import Base


class Admin(Base):
    __tablename__ = "admins"
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    name: str = Column(String(255), nullable=False)
    mail_address: str = Column(String(255), unique=True, nullable=False)
    password: str = Column(String(255), nullable=False)
    role = Column(Integer, nullable=False, default=1)
    __table_args__ = (CheckConstraint("role IN (1, 2, 3)", name="check_role_valid"),)

    class Config:
        orm_mode = True
