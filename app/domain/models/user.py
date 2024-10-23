import uuid

from db.database import Base

from pydantic import BaseModel
from sqlalchemy import UUID, VARCHAR, Column
from typing import Optional


class UserEntity(Base):
    __tablename__ = 'users'

    user_id = Column(UUID, primary_key=True, default=uuid.uuid4, nullable=False)
    user_name = Column(VARCHAR(75), nullable=False)
    user_surname = Column(VARCHAR(75), nullable=False)
    user_email = Column(VARCHAR(255), nullable=True)
    user_password = Column(VARCHAR(255), nullable=True)

class UserInDTO(BaseModel):
    name: str
    surname: str
    email: Optional[str]=None
    password: Optional[str]=None

class UserOutDTO(BaseModel):
    name: str
    surname: Optional[str]=None