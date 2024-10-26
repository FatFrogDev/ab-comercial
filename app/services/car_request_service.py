from domain.models.car_request import CarRequestEntity, CarRequestInDTO, CarRequestOutDTO, CarRequestUpdateDTO
from fastapi import HTTPException
from repositories.car_repository import CarRepository
from repositories.car_request_repository import CarRequestRepository
from repositories.locality_repository import LocalityRepository
from repositories.user_repository import UserRepository
from repositories.brand_repository import BrandRepository
from domain.models.brand import BrandEntity
from domain.models.car import CarEntity
from domain.models.locality import LocalityEntity
from domain.models.user import UserEntity
from sqlalchemy.orm import Session


class CarRequestService:
    
    def __init__(self, car_request_repository: CarRequestRepository, car_repository: CarRepository, locality_repository: LocalityRepository, user_repository: UserRepository, brand_repository: BrandRepository):
        self.car_request_repository = car_request_repository
        self.car_repository = car_repository
        self.locality_repository = locality_repository
        self.user_repository = user_repository
        self.brand_repository = brand_repository


    def save(self, db: Session, car_requestDTO: CarRequestInDTO):
        locality_entity = self.locality_repository.find_by_name(db, car_requestDTO.requested_at_locality)
        if locality_entity is None:
            locality_entity = self.locality_repository.save(db, LocalityEntity(locality_name=car_requestDTO.requested_at_locality))
        
        car_entity = self.car_repository.find_by_brand_name(db, car_requestDTO.car_requested)
        if car_entity is None:
            brand_entity = BrandEntity(brand_name=car_requestDTO.car_requested)
            brand_entity_saved = self.brand_repository.save(db, brand_entity)
            car_entity = CarEntity(brand=brand_entity_saved)
            car_entity = self.car_repository.save(db, car_entity)
        
        # Splits the name and surname of the user to search/save it in the database

        user_name = self.format_name_surname(car_requestDTO.user_requesting)[0]
        user_surname = self.format_name_surname(car_requestDTO.user_requesting)[1]

        user_entity = self.user_repository.find_by_name_and_surname(db, user_name, user_surname)

        if user_entity is None:
            user_entity = self.user_repository.save(db, UserEntity(user_name=user_name, user_surname=user_surname))
        
        car_request_entity = CarRequestEntity(car=car_entity, user=user_entity, locality=locality_entity)
        car_request_entity_saved = self.car_request_repository.save(db, car_request_entity)

        return CarRequestOutDTO(car_request_id=str(car_request_entity_saved.car_request_id),
                                request_date=car_request_entity_saved.request_date,
                                 user_requesting=self.merge_name_surname(car_request_entity_saved.user.user_name, car_request_entity_saved.user.user_surname),
                                user_id=str(car_request_entity_saved.user_requesting),
                                brand_id=car_request_entity_saved.car.brand.brand_id,
                                car_requested=str(car_request_entity_saved.car_requested),
                                requested_at_locality=car_request_entity_saved.locality.locality_name)
    

    def find_all_active(self, db: Session): 
        car_requests = self.car_request_repository.find_all_active(db)
        car_requests_response = []
        for car_request in car_requests:
            car_requests_response.append(CarRequestOutDTO(
                car_request_id=str(car_request.car_request_id),
                request_date=car_request.request_date,
                user_requesting=self.merge_name_surname(car_request.user.user_name, car_request.user.user_surname),
                user_id=str(car_request.user_requesting),
                brand_id=car_request.car.brand.brand_name,
                car_requested=str(car_request.car_requested),
                requested_at_locality=car_request.locality.locality_name))
        return car_requests_response


    """
        Updates a car request by id. It first checks if the car request exists, then it checks if the locality, car and user exist.
        Note: Car requested is a brand name given in the main view.
        For the car validation, it makes a brand name validation. If it exists its assigned to the request. If not, it creates it.
        Finally, its updates the car request with the new data.
    """
    

    def update_by_id(self, db: Session, car_request_id: str, car_requestDTO: CarRequestUpdateDTO):
        car_request_entity = self.car_request_repository.find_by_id(db, car_request_id)
        if car_request_entity is None:
            raise HTTPException(status_code=404, detail=f"Car request with id {car_request_id} not found")

        locality_entity = self.locality_repository.find_by_name(db, car_requestDTO.requested_at_locality)
        if locality_entity is None:
            locality_entity = self.locality_repository.save(db, LocalityEntity(locality_name=car_requestDTO.requested_at_locality))
        
        # Formats a name and finds the user by name and surname. If found its assigned to the entity. If not, its created and assigned it.
        user_name = self.format_name_surname(car_requestDTO.user_requesting)[0]
        user_surname = self.format_name_surname(car_requestDTO.user_requesting)[1]

        user_entity = self.user_repository.find_by_name_and_surname(db, user_name, user_surname)
        if user_entity is None:
            user_entity=self.user_repository.save(db, UserEntity(user_name=user_name, user_surname=user_surname))
        
        
        car_entity = self.car_repository.find_by_brand_name(db, car_requestDTO.car_requested)
        if car_entity is None:
            brand_entity = BrandEntity(brand_name=car_requestDTO.car_requested)
            brand_entity_saved = self.brand_repository.save(db, brand_entity)
            car_entity = CarEntity(brand=brand_entity_saved)
            car_entity = self.car_repository.save(db, car_entity)

        car_request_entity.request_date = car_request_entity.request_date
        car_request_entity.user_requesting = user_entity.user_id
        car_request_entity.car_requested = car_entity.car_id
        car_request_entity.requested_at_locality = locality_entity.locality_id

        updated_entity = self.car_request_repository.update(db, car_request_entity)
        return CarRequestOutDTO(car_request_id=str(updated_entity.car_request_id),
                                request_date=updated_entity.request_date,
                                user_requesting=self.merge_name_surname(updated_entity.user.user_name, updated_entity.user.user_surname),
                                user_id=str(updated_entity.user_requesting),
                                brand_id=updated_entity.car.brand.brand_id,
                                car_requested=updated_entity.car.brand.brand_name,
                                requested_at_locality=updated_entity.locality.locality_name)


    def find_by_id(self, db: Session, car_request_id: str):
        car_request_entity = self.car_request_repository.find_by_id_and_deleted_is_false(db, car_request_id)
        if car_request_entity is None:
            raise HTTPException(status_code=404, detail=f"Car request with id {car_request_id} not found")
        
        return CarRequestOutDTO(car_request_id=str(car_request_entity.car_request_id),
                                request_date=car_request_entity.request_date,
                                user_requesting=str(car_request_entity.user_requesting),
                                user_id=str(car_request_entity.user_requesting),
                                brand_id=car_request_entity.car.brand.brand_id,
                                car_requested=str(car_request_entity.car_requested),
                                requested_at_locality=car_request_entity.locality.locality_name)


    def delete_by_id(self, db: Session, car_request_id: str):
        car_request_entity = self.car_request_repository.find_by_id(db, car_request_id)
        if car_request_entity is None:
            raise HTTPException(status_code=404, detail=f"Car request with id {car_request_id} not found")
        if car_request_entity.deleted:
            raise HTTPException(status_code=400, detail=f"Car request with id {car_request_id} was already deleted.")
        self.car_request_repository.delete_by_id(db, car_request_id)


    def activate_by_id(self, db: Session, car_request_id: str):
        car_request_entity = self.car_request_repository.find_by_id(db, car_request_id)
        if car_request_entity is None:
            raise HTTPException(status_code=404, detail=f"Car request with id {car_request_id} not found")
        if not car_request_entity.deleted:
            raise HTTPException(status_code=400, detail=f"Car request with id {car_request_id} is already active.")
        self.car_request_repository.activate_by_id(db, car_request_id)


    def merge_name_surname(self, name: str, surname: str) -> str:
        return name.capitalize() + " " + surname.capitalize()
    

    def format_name_surname(self, name_surname:str):
        name_surname=name_surname.strip()
        name_surname = name_surname.split(" ")
        name = name_surname[0]
        surname = name_surname[1]
        return [name.capitalize(), surname.capitalize()]