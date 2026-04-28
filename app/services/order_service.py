from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.order import Order, OrderItem, OrderStatus
from app.models.product import Product
from app.schemas.order import OrderCreate


class OrderService:
    def __init__(self, db: Session):
        self.db = db

    def list_orders(self, user_id: int | None = None) -> list[Order]:
        query = self.db.query(Order)
        if user_id is not None:
            query = query.filter(Order.user_id == user_id)
        return query.order_by(Order.created_at.desc()).all()

    def get_order(self, order_id: int) -> Order:
        order = self.db.query(Order).filter(Order.id == order_id).first()
        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pedido não encontrado")
        return order

    def create_order(self, user_id: int, payload: OrderCreate) -> Order:
        order = Order(user_id=user_id, status=OrderStatus.PENDING, total=0.0)
        total = 0.0

        for item in payload.items:
            product = self.db.query(Product).filter(Product.id == item.product_id).first()
            if not product:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Produto {item.product_id} não encontrado",
                )
            if product.stock < item.quantity:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Estoque insuficiente para o produto '{product.name}'",
                )
            product.stock -= item.quantity
            order.items.append(
                OrderItem(product_id=product.id, quantity=item.quantity, unit_price=product.price)
            )
            total += product.price * item.quantity

        order.total = round(total, 2)
        self.db.add(order)
        self.db.commit()
        self.db.refresh(order)
        return order

    def update_status(self, order_id: int, new_status: OrderStatus) -> Order:
        order = self.get_order(order_id)
        order.status = new_status
        self.db.commit()
        self.db.refresh(order)
        return order

    def delete_order(self, order_id: int) -> None:
        order = self.get_order(order_id)
        self.db.delete(order)
        self.db.commit()
