from fastapi import Depends
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.models.order import Order, OrderStatus
from app.schemas.order import OrderCreate
from app.services.order_service import OrderService


class OrderController:
    def __init__(self, db: Session = Depends(get_db)):
        self.service = OrderService(db)

    def list_orders(self, user_id: int | None = None) -> list[Order]:
        return self.service.list_orders(user_id=user_id)

    def get_order(self, order_id: int) -> Order:
        return self.service.get_order(order_id)

    def create_order(self, user_id: int, payload: OrderCreate) -> Order:
        return self.service.create_order(user_id, payload)

    def update_status(self, order_id: int, new_status: OrderStatus) -> Order:
        return self.service.update_status(order_id, new_status)

    def delete_order(self, order_id: int) -> None:
        self.service.delete_order(order_id)
