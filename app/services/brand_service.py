from domain.models.brand import BrandDTO, BrandEntity
from fastapi import HTTPException
from repositories.brand_repository import BrandRepository
from sqlalchemy.orm import Session


class BrandService:
    
    def __init__(self, brand_repository: BrandRepository):
        self.brand_repository = brand_repository

    def save(self, db:Session, brandDTO: BrandDTO):
        brandDTO.brand_name = brandDTO.brand_name.strip()

        if self.brand_repository.find_brand_by_name(db, brandDTO.brand_name):
            raise HTTPException(status_code=400, detail=(f"Brand with name: {brandDTO.brand_name} already exists"))
            
        brand_response = self.brand_repository.save(db,  BrandEntity(brand_name=brandDTO.brand_name))

        return BrandDTO(brand_name=brand_response.brand_name)


    def find_brand_by_id(self, db:Session, brand_id: int):
        brand_entity = self.brand_repository.find_brand_by_id(db, brand_id)
        if brand_entity is None:
            raise HTTPException(status_code=404, detail=f"Brand with id: {brand_id} not found")
        return BrandDTO(brand_name=brand_entity.brand_name)


    def update_brand(self, db:Session, brand_id:int, brandDTO: BrandDTO):
        brand_entity = self.brand_repository.find_brand_by_id(db, brand_id)
        brand_exists_by_name = self.brand_repository.find_brand_by_name(db, brandDTO.brand_name)

        if brand_entity is None:
            raise HTTPException(status_code=404, detail=f"Brand with id: {brand_id} not found")

        if brand_exists_by_name:
            raise HTTPException(status_code=400, detail=f"Brand with name: {brandDTO.brand_name} already exists")

        brand_entity_updated=BrandEntity(brand_id=brand_id, brand_name=brandDTO.brand_name)

        return BrandDTO(brand_name=self.brand_repository.update_brand(db, brand_entity_updated).brand_name)