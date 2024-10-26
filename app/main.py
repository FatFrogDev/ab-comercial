from fastapi import FastAPI, APIRouter

from db.database import engine, Base
from fastapi.middleware.cors import CORSMiddleware

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

router = APIRouter()

app = FastAPI(
    title="MONITORING-INNOVATION-API",
    description="API prueba téncinca ab-comercial. Esta REST API contiene los endpoints escenciales para resolver la prueba técnica planteada por ab-comercial y varios adicionales. Desarrollado por Deyby Ariza",
    version="1.0",
    contact={
        "name":"Monitoring innovation",
        "url":"https://www.monitoringinnovation.com/"
    }    
)


origins=["http://localhost",
    "http://localhost:5173",
    "http://localhost:3000/"
    ]

# CORS Middleware config

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"]
)

# API Routers setup
app.include_router(locality_router)
app.include_router(brand_router)
app.include_router(car_router)
app.include_router(car_request_router)
app.include_router(user_router)

# Create the tables in the database with specified order to avoid foreign key constraints errors.

tables=[LocalityEntity.__table__, BrandEntity.__table__, CarEntity.__table__, UserEntity.__table__, CarRequestEntity.__table__]

Base.metadata.create_all(engine,tables=tables)