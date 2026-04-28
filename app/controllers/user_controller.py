from fastapi import Depends
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserPatch, UserUpdate
from app.services.user_service import UserService


class UserController:
    def __init__(self, db: Session = Depends(get_db)):
        self.service = UserService(db)

    def list_users(self, skip: int = 0, limit: int = 100) -> list[User]:
        return self.service.list_users(skip=skip, limit=limit)

    def get_user(self, user_id: int) -> User:
        return self.service.get_user(user_id)

    def create_user(self, payload: UserCreate) -> User:
        return self.service.create_user(payload)

    def replace_user(self, user_id: int, payload: UserUpdate) -> User:
        return self.service.replace_user(user_id, payload)

    def patch_user(self, user_id: int, payload: UserPatch) -> User:
        return self.service.patch_user(user_id, payload)

    def delete_user(self, user_id: int) -> None:
        self.service.delete_user(user_id)
