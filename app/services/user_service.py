from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate, UserPatch, UserUpdate
from app.utils.security import hash_password


class UserService:
    def __init__(self, db: Session):
        self.db = db

    def list_users(self, skip: int = 0, limit: int = 100) -> list[User]:
        return self.db.query(User).offset(skip).limit(limit).all()

    def get_user(self, user_id: int) -> User:
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")
        return user

    def create_user(self, payload: UserCreate, is_admin: bool = False) -> User:
        if self.db.query(User).filter(User.email == payload.email).first():
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="E-mail já cadastrado")
        user = User(
            name=payload.name,
            email=payload.email,
            hashed_password=hash_password(payload.password),
            is_admin=is_admin,
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def replace_user(self, user_id: int, payload: UserUpdate) -> User:
        user = self.get_user(user_id)
        if payload.email != user.email and self.db.query(User).filter(User.email == payload.email).first():
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="E-mail já cadastrado")
        user.name = payload.name
        user.email = payload.email
        user.hashed_password = hash_password(payload.password)
        self.db.commit()
        self.db.refresh(user)
        return user

    def patch_user(self, user_id: int, payload: UserPatch) -> User:
        user = self.get_user(user_id)
        data = payload.model_dump(exclude_unset=True)

        if "email" in data and data["email"] != user.email:
            if self.db.query(User).filter(User.email == data["email"]).first():
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="E-mail já cadastrado")
            user.email = data["email"]
        if "name" in data:
            user.name = data["name"]
        if "password" in data and data["password"]:
            user.hashed_password = hash_password(data["password"])
        if "is_active" in data:
            user.is_active = data["is_active"]

        self.db.commit()
        self.db.refresh(user)
        return user

    def delete_user(self, user_id: int) -> None:
        user = self.get_user(user_id)
        self.db.delete(user)
        self.db.commit()
