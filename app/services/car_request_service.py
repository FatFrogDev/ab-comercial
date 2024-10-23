from domain.models.car_request import CarRequestEntity, CarRequestInDTO, CarRequestOutDTO
from fastapi import HTTPException
from repositories.car_repository import CarRepository
from repositories.car_request_repository import CarRequestRepository
from repositories.locality_repository import LocalityRepository
from repositories.user_repository import UserRepository
from sqlalchemy.orm import Session


class CarRequestService:
    
    def __init__(self, car_request_repository: CarRequestRepository, car_repository: CarRepository, locality_repository:LocalityRepository, user_repository: UserRepository):
        self.car_request_repository = car_request_repository
        self.car_repository = car_repository
        self.locality_repository = locality_repository
        self.user_repository = user_repository
    

    def save(self, db: Session, car_requestDTO: CarRequestInDTO):
        locality_entity = self.locality_repository.find_by_name(db, car_requestDTO.requested_at_locality)

        if locality_entity is None:
            raise HTTPException(status_code=404, detail=f"Locality {car_requestDTO.requested_at_locality} not found")

        car_entity = self.car_repository.find_by_id(db, car_requestDTO.car_requested)

        if car_entity is None:
            raise HTTPException(status_code=404, detail=f"Car wit id {car_requestDTO.car_requested} not found")
        
        user_entity = self.user_repository.find_user_by_id(db, car_requestDTO.user_requesting)

        if user_entity is None:
            raise HTTPException(status_code=404, detail=f"User with id {car_requestDTO.user_requesting} not found")
        
        car_entity = CarRequestEntity(car=car_entity, user_requesting=user_entity,
                                      user=user_entity, locality=locality_entity)
        
        car_entity_saved = self.car_request_repository.save(db, car_entity)

        return CarRequestOutDTO(car_request_id=str(car_entity_saved.car_request_id),
                         request_date=car_entity_saved.request_date,
                         user_requesting=str(car_entity_saved.user_requesting),
                         car_requested=str(car_entity_saved.car_requested),
                         requested_at_locality=car_entity_saved.locality.locality_name)


    def find_all_active(self, db: Session): 
        car_requests = self.car_request_repository.find_all_active(db)
        car_requests_response = []
        for car_request in car_requests:
            car_requests_response.append(CarRequestOutDTO(car_request_id=str(car_request.car_request_id),
                                                          request_date=car_request.request_date,
                                                          user_requesting=self.merge_name_surname(car_request.user.user_name, car_request.user.user_surname),
                                                          car_requested=car_request.car.brand.brand_name,
                                                          requested_at_locality=car_request.locality.locality_name))
        return car_requests_response


    def find_by_id(self, db: Session, car_request_id):
        car_request_entity = self.car_request_repository.find_by_id_and_deleted_is_false(db, car_request_id)
        if car_request_entity is None:
            raise HTTPException(status_code=404, detail=f"Car request with id {car_request_id} not found")
        
        car_response = CarRequestOutDTO(car_request_id=str(car_request_entity.car_request_id),
                                        request_date=car_request_entity.request_date,
                                        user_requesting=str(car_request_entity.user_requesting),
                                        car_requested=str(car_request_entity.car_requested),
                                        requested_at_locality=car_request_entity.locality.locality_name)
        return car_response


    def delete_by_id(self, db: Session, car_request_id):
        car_request_entity = self.car_request_repository.find_by_id(db, car_request_id)

        if car_request_entity is None:
            raise HTTPException(status_code=404, detail=f"Car request with id {car_request_id} not found")

        if car_request_entity.deleted:
            raise HTTPException(status_code=400, detail=f"Car request with id {car_request_id} was already deleted.")

        self.car_request_repository.delete_by_id(db, car_request_id)


    def activate_by_id(self, db: Session, car_request_id):
        car_request_entity = self.car_request_repository.find_by_id(db, car_request_id)

        if car_request_entity is None:
            raise HTTPException(status_code=404, detail=f"Car request with id {car_request_id} not found")

        if not car_request_entity.deleted:
            raise HTTPException(status_code=400, detail=f"Car request with id {car_request_id} is already active.")

        self.car_request_repository.activate_by_id(db, car_request_id)
    
    
    
    # Capitalizes the first letter of the name and surname
    def merge_name_surname(self, name, surname):
        name = name[0].upper() + name[1:]
        surname = surname[0].upper() + surname[1:]
        return name + " " + surname