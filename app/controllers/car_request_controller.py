from db.database import get_db
from domain.models.car_request import CarRequestInDTO, CarRequestOutDTO
from fastapi import APIRouter, Depends
from repositories.car_repository import CarRepository
from repositories.car_request_repository import CarRequestRepository
from repositories.locality_repository import LocalityRepository
from repositories.user_repository import UserRepository
from services.car_request_service import CarRequestService
from sqlalchemy.orm import Session

router = APIRouter()

brand_repository = CarRepository()
locality_repository = LocalityRepository()
user_repository = UserRepository()
car_request_repository = CarRequestRepository()
car_request_service = CarRequestService(car_request_repository, brand_repository, locality_repository, user_repository)

@router.post("/api/v1/car-requests/save", response_model=CarRequestOutDTO, status_code=201)
def save(car_request: CarRequestInDTO, db: Session = Depends(get_db)):
    return car_request_service.save(db, car_request)


@router.get("/api/v1/car-requests/all", response_model=list[CarRequestOutDTO], status_code=200)
def find_all(db: Session = Depends(get_db)):    
    return car_request_service.find_all_active(db)


@router.get("/api/v1/car-requests/{car_request_id}", response_model=CarRequestOutDTO, status_code=200)
def find_by_id(car_request_id: str, db: Session = Depends(get_db)):
    return car_request_service.find_by_id(db, car_request_id)


@router.delete("/api/v1/car-requests/{car_request_id}", status_code=204)
def delete_by_id(car_request_id: str, db: Session = Depends(get_db)):
    car_request_service.delete_by_id(db, car_request_id)


@router.put("/api/v1/car-requests/{car_request_id}", response_model=CarRequestOutDTO, status_code=200)
def update(car_request_id: str, car_request: CarRequestInDTO, db: Session = Depends(get_db)):
    return car_request_service.update(db, car_request_id, car_request)


@router.patch("/api/v1/car-requests/{car_request_id}/activate", status_code=204)
def activate_by_id(car_request_id: str, db: Session = Depends(get_db)):
    car_request_service.activate_by_id(db, car_request_id)