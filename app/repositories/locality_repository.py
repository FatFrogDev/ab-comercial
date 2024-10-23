from sqlalchemy.orm import Session
from domain.models.locality import LocalityDTO, LocalityEntity

class LocalityRepository:

    def save(self, db: Session, locality: LocalityEntity):
        db.add(locality)
        db.commit()
        db.refresh(locality)
        return locality

    def locality_exists_by_name(self, db: Session, locality_name: str):
        result = db.query(LocalityEntity).filter(LocalityEntity.locality_name == locality_name).first()
        return result is not None

    def find_by_name(self, db: Session, locality_name: str):
        
        locality_name = locality_name.strip().lower()
        return db.query(LocalityEntity).filter(LocalityEntity.locality_name == locality_name).first()

        