from fastapi import APIRouter, Depends, status

from app.controllers.user_controller import UserController
from app.models.user import User
from app.schemas.user import UserCreate, UserOut, UserPatch, UserUpdate
from app.utils.helpers import get_current_user, require_admin

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register_user(payload: UserCreate, controller: UserController = Depends()):
    return controller.create_user(payload)


@router.get("", response_model=list[UserOut], dependencies=[Depends(require_admin)])
def list_users(skip: int = 0, limit: int = 100, controller: UserController = Depends()):
    return controller.list_users(skip=skip, limit=limit)


@router.get("/me", response_model=UserOut)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.get("/{user_id}", response_model=UserOut, dependencies=[Depends(require_admin)])
def get_user(user_id: int, controller: UserController = Depends()):
    return controller.get_user(user_id)


@router.put("/{user_id}", response_model=UserOut, dependencies=[Depends(require_admin)])
def replace_user(user_id: int, payload: UserUpdate, controller: UserController = Depends()):
    return controller.replace_user(user_id, payload)


@router.patch("/{user_id}", response_model=UserOut, dependencies=[Depends(require_admin)])
def patch_user(user_id: int, payload: UserPatch, controller: UserController = Depends()):
    return controller.patch_user(user_id, payload)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_admin)])
def delete_user(user_id: int, controller: UserController = Depends()):
    controller.delete_user(user_id)
