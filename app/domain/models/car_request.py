import datetime
import uuid

from db.database import Base
from domain.models.car import CarEntity
from domain.models.locality import LocalityEntity
from domain.models.user import UserEntity
from pydantic import BaseModel
from sqlalchemy import (UUID, BigInteger, Boolean, Column, Date, ForeignKey,
                        Integer, String, Table)
from sqlalchemy.orm import declarative_base as declarative_base
from sqlalchemy.orm import relationship
from typing import Optional


Base = declarative_base()


class CarRequestEntity(Base):
    __tablename__ = 'car_requests'

    car_request_id = Column(UUID, primary_key=True, default=uuid.uuid4, nullable=False)
    request_date = Column(Date, nullable=False, default=datetime.datetime.now())  
    deleted = Column(Boolean, nullable=False, default=False)

    # Relationships
    user_requesting = Column(UUID, ForeignKey(UserEntity.user_id), nullable=False)
    car_requested = Column(UUID, ForeignKey(CarEntity.car_id), nullable=False)
    requested_at_locality = Column(BigInteger, ForeignKey(LocalityEntity.locality_id), nullable=False)
    
    user = relationship(UserEntity, backref="car_requests")
    car = relationship(CarEntity, backref="car_requests")
    locality = relationship(LocalityEntity, backref="car_requests")


class CarRequestInDTO(BaseModel):
    car_request_id: Optional[str]=None
    user_requesting: str
    car_requested: str
    requested_at_locality: str

class CarRequestOutDTO(BaseModel):
    car_request_id: Optional[str]=None
    request_date: datetime.date
    user_requesting: str
    user_id: str
    brand_id: int | str
    car_requested: str
    requested_at_locality: str

class CarRequestUpdateDTO(BaseModel):
    car_requested: Optional[str]=None
    user_requesting: str
    user_id: Optional[str]=None
    requested_at_locality: str    