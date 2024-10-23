from sqlalchemy import UUID, Column, Date, ForeignKey, Integer, String, BigInteger, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base as declarative_base
from typing import Optional

import uuid
from db.database import Base
from pydantic import BaseModel

import uuid
from db.database import Base
from pydantic import BaseModel

Base = declarative_base()

class LocalityEntity(Base):
    __tablename__ = "localities"

    locality_id = Column(BigInteger, primary_key=True, index=True, nullable=False) # Default db type: BIGSERIAL
    locality_name = Column(VARCHAR(100), nullable=False)



class LocalityDTO(BaseModel):
    locality_id: Optional[int]=None
    locality_name: str