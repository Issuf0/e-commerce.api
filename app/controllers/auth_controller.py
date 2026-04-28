from fastapi import Depends
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.schemas.auth import LoginRequest, Token
from app.services.auth_service import AuthService


class AuthController:
    def __init__(self, db: Session = Depends(get_db)):
        self.service = AuthService(db)

    def login(self, payload: LoginRequest) -> Token:
        return self.service.login(payload)
