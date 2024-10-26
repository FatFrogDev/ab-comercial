from domain.models.car import CarEntity
from domain.models.brand import BrandEntity
from sqlalchemy.orm import Session
from sqlalchemy import select

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
    
    # TODO: Clarify in the docs that was made this way due the face.

    def find_by_brand_id(self, db: Session, brand_id: str):
            return db.query(CarEntity).filter(CarEntity.brand_id == brand_id).first()
    
    def find_by_brand_name(self, db: Session, brand_name: str):
               # Realizamos la consulta usando una unión para filtrar por el nombre de la marca
        return db.query(CarEntity).join(CarEntity.brand).where(BrandEntity.brand_name == brand_name).first()
        # Ejecutamos la consulta y retornamos los resultados
    