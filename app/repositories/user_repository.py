from domain.models.user import UserEntity
from sqlalchemy.orm import Session


class UserRepository:

    def save(self, db:Session, user: UserEntity):
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    
    def find_user_by_id(self, db: Session, user_id: str):
        return db.query(UserEntity).filter(UserEntity.user_id == user_id).first()