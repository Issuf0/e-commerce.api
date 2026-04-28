from fastapi import Depends
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductPatch, ProductUpdate
from app.services.product_service import ProductService


class ProductController:
    def __init__(self, db: Session = Depends(get_db)):
        self.service = ProductService(db)

    def list_products(self, skip: int = 0, limit: int = 100, q: str | None = None) -> list[Product]:
        return self.service.list_products(skip=skip, limit=limit, q=q)

    def get_product(self, product_id: int) -> Product:
        return self.service.get_product(product_id)

    def create_product(self, payload: ProductCreate) -> Product:
        return self.service.create_product(payload)

    def replace_product(self, product_id: int, payload: ProductUpdate) -> Product:
        return self.service.replace_product(product_id, payload)

    def patch_product(self, product_id: int, payload: ProductPatch) -> Product:
        return self.service.patch_product(product_id, payload)

    def delete_product(self, product_id: int) -> None:
        self.service.delete_product(product_id)
