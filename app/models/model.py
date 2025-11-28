from app.db.database import Base
from sqlalchemy import Column, Integer, String
from pydantic import BaseModel, Field

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique= True)
    hashed_password = Column(String)
    name = Column(String)
    email = Column(String, unique=True)


