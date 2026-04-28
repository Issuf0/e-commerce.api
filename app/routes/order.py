from fastapi import APIRouter, Depends, HTTPException, status

from app.controllers.order_controller import OrderController
from app.models.user import User
from app.schemas.order import OrderCreate, OrderOut, OrderStatusUpdate
from app.utils.helpers import get_current_user, require_admin

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.get("", response_model=list[OrderOut])
def list_orders(
    controller: OrderController = Depends(),
    current_user: User = Depends(get_current_user),
):
    user_filter = None if current_user.is_admin else current_user.id
    return controller.list_orders(user_id=user_filter)


@router.get("/{order_id}", response_model=OrderOut)
def get_order(
    order_id: int,
    controller: OrderController = Depends(),
    current_user: User = Depends(get_current_user),
):
    order = controller.get_order(order_id)
    if not current_user.is_admin and order.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acesso negado a este pedido")
    return order


@router.post("", response_model=OrderOut, status_code=status.HTTP_201_CREATED)
def create_order(
    payload: OrderCreate,
    controller: OrderController = Depends(),
    current_user: User = Depends(get_current_user),
):
    return controller.create_order(current_user.id, payload)


@router.put("/{order_id}/status", response_model=OrderOut, dependencies=[Depends(require_admin)])
def replace_order_status(
    order_id: int,
    payload: OrderStatusUpdate,
    controller: OrderController = Depends(),
):
    return controller.update_status(order_id, payload.status)


@router.patch("/{order_id}/status", response_model=OrderOut, dependencies=[Depends(require_admin)])
def patch_order_status(
    order_id: int,
    payload: OrderStatusUpdate,
    controller: OrderController = Depends(),
):
    return controller.update_status(order_id, payload.status)


@router.delete(
    "/{order_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_admin)],
)
def delete_order(order_id: int, controller: OrderController = Depends()):
    controller.delete_order(order_id)
