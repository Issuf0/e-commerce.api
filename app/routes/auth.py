from fastapi import APIRouter, Depends

from app.controllers.auth_controller import AuthController
from app.schemas.auth import LoginRequest, Token

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=Token)
def login(payload: LoginRequest, controller: AuthController = Depends()):
    return controller.login(payload)
