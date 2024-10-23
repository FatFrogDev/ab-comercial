from sqlalchemy.orm import Session
from domain.models.brand import BrandEntity

class BrandRepository:

    def save(self, db:Session, brand: BrandEntity):
        db.add(brand)
        db.commit()
        db.refresh(brand)
        return brand
    
    def find_brand_by_id(self, db: Session, brand_id: int):
        return db.query(BrandEntity).filter(BrandEntity.brand_id == brand_id).first()
    
    def update_brand(self, db: Session, brand: BrandEntity):
        db.query(BrandEntity).filter(BrandEntity.brand_id == brand.brand_id).update(
            {BrandEntity.brand_id: brand.brand_id,
             BrandEntity.brand_name: brand.brand_name})
        db.commit()
        return brand

    def find_brand_by_name(self, db: Session, brand_name: str):
        return db.query(BrandEntity).filter(BrandEntity.brand_name == brand_name).first()

    def brand_exists_by_id(self, db: Session, brand_id: int):
        return db.query(BrandEntity).filter(BrandEntity.brand_id == brand_id).first() is not None
