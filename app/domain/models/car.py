import uuid
from typing import Optional

from db.database import Base
from domain.models.brand import BrandEntity
from pydantic import BaseModel
from sqlalchemy import (UUID, VARCHAR, BigInteger, Column, Date, ForeignKey,
                        String, Table)
from sqlalchemy.orm import declarative_base as declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class CarEntity(Base):
    __tablename__ = 'cars'

    car_id = Column(UUID, primary_key=True, default=uuid.uuid4, nullable=False)
    car_plate = Column(VARCHAR(255), nullable=False)
    car_cc = Column(VARCHAR(20))
    car_name=Column(VARCHAR(60))
    # Relationships
    brand_id = Column(BigInteger, ForeignKey(BrandEntity.brand_id), nullable=False)
    brand = relationship(BrandEntity, backref="cars")

class CarInDTO(BaseModel):
    car_plate: Optional[str]=None
    car_name: Optional[str]=None
    car_cc: Optional[str]=None
    brand_id: int

class CarOutDTO(BaseModel):
    car_plate: str
    car_cc: str
    brand_name: str
