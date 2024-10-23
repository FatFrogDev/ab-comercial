from db.database import get_db
from domain.models.user import UserInDTO, UserOutDTO
from fastapi import APIRouter, Depends
from repositories.user_repository import UserRepository
from services.user_service import UserService
from sqlalchemy.orm import Session

router = APIRouter()

user_repository = UserRepository()
user_service = UserService(user_repository)

@router.post("/api/v1/users/save", response_model=UserOutDTO, status_code=201)
def save_user(user: UserInDTO, db: Session = Depends(get_db)):
    return user_service.save(db, user)

@router.get("/api/v1/users/{user_id}", response_model=UserOutDTO, status_code=200)
def find_by_id(user_id: str, db: Session = Depends(get_db)):
    return user_service.find_by_id(db, user_id)