from fastapi import APIRouter, Depends

from repositories.brand_repository import BrandRepository
from services.brand_service import BrandService
from domain.models.brand import BrandDTO

from sqlalchemy.orm import Session

from db.database import get_db

router = APIRouter()

brand_repository = BrandRepository()
brand_service = BrandService(brand_repository)

@router.post("/api/v1/brands/save", response_model=BrandDTO, status_code=201)
def save_brand(brandDTO: BrandDTO, db: Session = Depends(get_db)):
    return brand_service.save(db, brandDTO)

@router.get("/api/v1/brands/{brand_id}", response_model=BrandDTO, status_code=200)
def find_by_id(brand_id: int, db: Session = Depends(get_db)):
    return brand_service.find_brand_by_id(db, brand_id)

@router.patch("/api/v1/brands/{brand_id}/update", response_model=BrandDTO, status_code=200)
def update_brand(brand_id:str, brandDTO: BrandDTO, db: Session = Depends(get_db)):
   return brand_service.update_brand(db, brand_id, brandDTO)