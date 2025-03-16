from sqlalchemy import Boolean, Column, Integer, String

from db.base_class import Base


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String)
    is_active = Column(Boolean(), default=True)
    hashed_password = Column(String)
    hashed_password = Column(String)
