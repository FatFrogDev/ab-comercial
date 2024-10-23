from fastapi import FastAPI, APIRouter

from db.database import engine, Base

from controllers.locality_controller import router as locality_router
from controllers.brand_controller import router as brand_router
from controllers.car_controller import router as car_router
from controllers.car_request_controller import router as car_request_router
from controllers.user_controller import router as user_router

from domain.models.brand import BrandEntity
from domain.models.car import CarEntity
from domain.models.car_request import CarRequestEntity
from domain.models.locality import LocalityEntity
from domain.models.user import UserEntity


app = FastAPI()
router = APIRouter()

# Create the tables with specified order to avoid foreign key constraints errors.
Base.metadata.create_all(engine, tables=[LocalityEntity.__table__, BrandEntity.__table__, 
                                        CarEntity.__table__, UserEntity.__table__, CarRequestEntity.__table__])

# API Routers setup
app.include_router(locality_router)
app.include_router(brand_router)
app.include_router(car_router)
app.include_router(car_request_router)
app.include_router(user_router)