from fastapi import APIRouter, Depends, status

from app.controllers.product_controller import ProductController
from app.schemas.product import ProductCreate, ProductOut, ProductPatch, ProductUpdate
from app.utils.helpers import require_admin

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("", response_model=list[ProductOut])
def list_products(
    skip: int = 0,
    limit: int = 100,
    q: str | None = None,
    controller: ProductController = Depends(),
):
    return controller.list_products(skip=skip, limit=limit, q=q)


@router.get("/{product_id}", response_model=ProductOut)
def get_product(product_id: int, controller: ProductController = Depends()):
    return controller.get_product(product_id)


@router.post(
    "",
    response_model=ProductOut,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_admin)],
)
def create_product(payload: ProductCreate, controller: ProductController = Depends()):
    return controller.create_product(payload)


@router.put("/{product_id}", response_model=ProductOut, dependencies=[Depends(require_admin)])
def replace_product(product_id: int, payload: ProductUpdate, controller: ProductController = Depends()):
    return controller.replace_product(product_id, payload)


@router.patch("/{product_id}", response_model=ProductOut, dependencies=[Depends(require_admin)])
def patch_product(product_id: int, payload: ProductPatch, controller: ProductController = Depends()):
    return controller.patch_product(product_id, payload)


@router.delete(
    "/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_admin)],
)
def delete_product(product_id: int, controller: ProductController = Depends()):
    controller.delete_product(product_id)
