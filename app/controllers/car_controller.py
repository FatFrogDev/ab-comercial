from fastapi import APIRouter,Depends

from services.car_service import CarService

from repositories.car_repository import CarRepository
from repositories.brand_repository import BrandRepository

from domain.models.car import CarInDTO, CarOutDTO

from sqlalchemy.orm import Session

from db.database import get_db

router = APIRouter()

car_repository = CarRepository()
brand_repository = BrandRepository()
car_service= CarService(car_repository, brand_repository)

@router.post("/api/v1/cars/save", response_model=CarOutDTO, status_code=201)
def save_car(carInDTO: CarInDTO, db: Session = Depends(get_db)):
    return car_service.save(db, carInDTO)

@router.get("/api/v1/cars/{car_id}", response_model=CarOutDTO, status_code=200)
def find_car_by_id(car_id: str, db: Session = Depends(get_db)):
    return car_service.find_by_id(db, car_id)

@router.get("/api/v1/cars/plate/{plate}", response_model=CarOutDTO, status_code=200)
def find_car_by_plate(plate: str, db: Session = Depends(get_db)):
    return car_service.find_by_plate(db, plate)
