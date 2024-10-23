from fastapi import APIRouter,Depends

from repositories.locality_repository import LocalityRepository
from services.locality_service import LocalityService

from domain.models.locality import LocalityDTO

from sqlalchemy.orm import Session

from db.database import get_db

router = APIRouter()

locality_repository = LocalityRepository()
locality_service = LocalityService(locality_repository)

@router.post("/api/v1/localities/save", response_model=LocalityDTO, status_code=201)
def save_locality(locality: LocalityDTO, db: Session = Depends(get_db)):
    return locality_service.save(db, locality)

@router.get("/api/v1/localities/{locality_name}", response_model=LocalityDTO, status_code=200)
def find_locality_by_name(locality_name: str, db: Session = Depends(get_db)):
    return locality_service.find_by_name(db, locality_name)