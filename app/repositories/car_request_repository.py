from domain.models.car_request import CarRequestEntity
from sqlalchemy.orm import Session



class CarRequestRepository:
    
    def save(self, db: Session, car_request_entity: CarRequestEntity):
        db.add(car_request_entity)
        db.commit()
        db.refresh(car_request_entity)
        return car_request_entity

    def find_all_active(self, db: Session):
        return db.query(CarRequestEntity).filter(CarRequestEntity.deleted == False).all()


    def find_by_id_and_deleted_is_false(self, db: Session, car_request_id: str):
        return db.query(CarRequestEntity).filter(CarRequestEntity.car_request_id == car_request_id).filter(CarRequestEntity.deleted == False).first()


    def find_by_id(self, db: Session, car_request_id: str):
        return db.query(CarRequestEntity).filter(CarRequestEntity.car_request_id == car_request_id).first()


    def update(self, db: Session, car_request_entity: CarRequestEntity):
        db.query(CarRequestEntity).filter(CarRequestEntity.car_request_id == car_request_entity.car_request_id).update(
            {
            CarRequestEntity.request_date: car_request_entity.request_date,
            CarRequestEntity.user_requesting: car_request_entity.user_requesting,
            CarRequestEntity.car_requested: car_request_entity.car_requested,
            CarRequestEntity.requested_at_locality: car_request_entity.requested_at_locality})
        db.commit()
        return car_request_entity


    def delete_by_id(self, db: Session, id: str):
        db.query(CarRequestEntity).filter(CarRequestEntity.car_request_id == id).update({CarRequestEntity.deleted: True})
        db.commit()


    def activate_by_id(self, db: Session, id: str):
        db.query(CarRequestEntity).filter(CarRequestEntity.car_request_id == id).update({CarRequestEntity.deleted: False})
        db.commit()