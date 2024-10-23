import bcrypt, uuid
from fastapi import HTTPException
from sqlalchemy.orm import Session

from domain.models.user import UserEntity, UserInDTO, UserOutDTO

from repositories.user_repository import UserRepository


class UserService:

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def save(self, db: Session, user_in: UserInDTO):
        hashed_password = None
        if user_in.password is not None:
            hashed_password = bcrypt.hashpw(user_in.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        user_in.name = user_in.name.lower()
        user_in.surname = user_in.surname.lower()

        user = UserEntity(
            user_name=user_in.name,
            user_surname=user_in.surname,
            user_email=user_in.email,
            user_password=hashed_password)
        
        user_response =  self.user_repository.save(db, user)

        user_out = UserOutDTO(
            name=user_response.user_name,
            surname=user_response.user_surname)
            
        return user_out


        return 

    def find_by_id(self, db: Session, user_id: int):
        user = self.user_repository.find_user_by_id(db, user_id)

        if user is None:
            raise HTTPException(status_code=404, detail=(f"User wit id {user_id} not found"))

        return UserOutDTO(
            name=user.user_name[0].upper() + user.user_name[1:],
            surname=user.user_surname[0].upper() + user.user_surname[1:])

    def merge_name_surname(self, name: str, surname: str):
        name = name[0].upper() + name[1:]
        surname = surname[0].upper() + surname[1:]
        return f"{name} {surname}"