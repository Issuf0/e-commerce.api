from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.product import Product
from app.schemas.product import ProductCreate, ProductPatch, ProductUpdate


class ProductService:
    def __init__(self, db: Session):
        self.db = db

    def list_products(self, skip: int = 0, limit: int = 100, q: str | None = None) -> list[Product]:
        query = self.db.query(Product)
        if q:
            query = query.filter(Product.name.ilike(f"%{q}%"))
        return query.offset(skip).limit(limit).all()

    def get_product(self, product_id: int) -> Product:
        product = self.db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto não encontrado")
        return product

    def create_product(self, payload: ProductCreate) -> Product:
        product = Product(**payload.model_dump())
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        return product

    def replace_product(self, product_id: int, payload: ProductUpdate) -> Product:
        product = self.get_product(product_id)
        for field, value in payload.model_dump().items():
            setattr(product, field, value)
        self.db.commit()
        self.db.refresh(product)
        return product

    def patch_product(self, product_id: int, payload: ProductPatch) -> Product:
        product = self.get_product(product_id)
        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(product, field, value)
        self.db.commit()
        self.db.refresh(product)
        return product

    def delete_product(self, product_id: int) -> None:
        product = self.get_product(product_id)
        self.db.delete(product)
        self.db.commit()
