from domain.models.locality import LocalityDTO, LocalityEntity
from fastapi import HTTPException
from repositories.locality_repository import LocalityRepository
from sqlalchemy.orm import Session


class LocalityService:

    def __init__(self, locality_repository: LocalityRepository):
        self.locality_repository = locality_repository

    def save(self, db : Session, localityDTO:LocalityDTO):
        localityDTO.locality_name = localityDTO.locality_name.strip() 
        localityDTO.locality_name = localityDTO.locality_name.lower()

        if localityDTO.locality_name.__contains__(" "):
            localityDTO.locality_name = localityDTO.locality_name.replace(" ", "-")

        locality_exists = self.locality_repository.locality_exists_by_name(db, localityDTO.locality_name)
        
        if locality_exists:
            raise HTTPException(status_code=400, detail=f"Locality with name: {localityDTO.locality_name} already exists")

        locality_entity = LocalityEntity(locality_name=localityDTO.locality_name)
        return self.locality_repository.save(db, locality_entity)


    def find_by_name(self, db : Session, locality_name: str):
        locality_name = locality_name.strip()

        if locality_name.__contains__(" "):
            locality_name = locality_name.replace(" ", "-")

        locality_entity = self.locality_repository.find_by_name(db, locality_name)
        
        if locality_entity is None:
            raise HTTPException(status_code=404, detail=f"Locality with name: {locality_name} not found")
        
        return LocalityDTO(locality_id=locality_entity.locality_id, locality_name=locality_entity.locality_name)