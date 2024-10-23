import uuid

from sqlalchemy.orm import declarative_base as declarative_base

from db.database import Base
from pydantic import BaseModel
from sqlalchemy import UUID, Column, Date, ForeignKey, BigInteger, String, VARCHAR, Table
from sqlalchemy.orm import relationship

Base = declarative_base()

class BrandEntity(Base):
    __tablename__ = 'brands'  
    
    brand_id = Column(BigInteger, primary_key=True, nullable=False, autoincrement=True)
    brand_name = Column(VARCHAR(255), nullable=False, unique=True)

class BrandDTO(BaseModel):
    brand_name: str