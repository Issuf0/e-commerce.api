from fastapi import APIRouter

from app.routes.auth import router as auth_router
from app.routes.order import router as order_router
from app.routes.product import router as product_router
from app.routes.user import router as user_router

api_router = APIRouter()
api_router.include_router(auth_router)
api_router.include_router(user_router)
api_router.include_router(product_router)
api_router.include_router(order_router)
