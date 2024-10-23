from domain.models.car import CarEntity
from sqlalchemy.orm import Session


class CarRepository:

    def save(self, db: Session, car_entity: CarEntity):
        db.add(car_entity)
        db.commit()
        db.refresh(car_entity)
        return car_entity

    def find_by_id(self, db: Session, car_id: str):
        return db.query(CarEntity).filter(CarEntity.car_id == car_id).first()

    def find_by_plate(self, db: Session, plate: str):
        return db.query(CarEntity).filter(CarEntity.car_plate == plate).first()