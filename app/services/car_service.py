from domain.models.car import CarEntity, CarInDTO, CarOutDTO
from fastapi import HTTPException
from repositories.brand_repository import BrandRepository
from repositories.car_repository import CarRepository


class CarService:

    def __init__(self, car_repository: CarRepository, brand_repository: BrandRepository):
        self.car_repository = car_repository
        self.brand_repository = brand_repository

    def save(self, db, carInDTO:CarInDTO):
        carInDTO.car_plate = carInDTO.car_plate.upper()
        car_exists_by_plate = self.car_repository.find_by_plate(db, carInDTO.car_plate)

        if car_exists_by_plate:
            raise HTTPException(status_code=400, detail=f"Car with plate {carInDTO.car_plate} already exists")

        brand_entity = self.brand_repository.find_brand_by_id(db, carInDTO.brand_id)

        if brand_entity is None:
            raise HTTPException(status_code=400, detail="Brand not found")

        car_entity = CarEntity(
            car_plate=carInDTO.car_plate, car_name=carInDTO.car_name,
            car_cc=carInDTO.car_cc,
            brand=brand_entity)
        
        car_response = self.car_repository.save(db, car_entity)

        return CarOutDTO(car_plate=car_response.car_plate,
                         car_cc=car_response.car_cc, brand_name=brand_entity.brand_name)

    def find_by_id(self, db, car_id):
        car_response = self.car_repository.find_by_id(db, car_id)
        if car_response is None:
            raise HTTPException(status_code=404, detail=f"Car with id {car_id} not found")
        return CarOutDTO(car_plate=car_response.car_plate, car_cc=car_response.car_cc,
                         brand_name=car_response.brand.brand_name)

    def find_by_plate(self, db, plate):
        car_response = self.car_repository.find_by_plate(db, plate)
        return CarOutDTO(car_plate=car_response.car_plate,car_cc=car_response.car_cc,
                         brand_name=car_response.brand.brand_name)
    