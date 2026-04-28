from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.config.database import Base, SessionLocal, engine
from app.models import User
from app.routes import api_router
from app.utils.security import hash_password


def _bootstrap_admin() -> None:
    db = SessionLocal()
    try:
        if db.query(User).filter(User.is_admin.is_(True)).first():
            return
        admin = User(
            name="Admin",
            email="admin@ecommerce.com",
            hashed_password=hash_password("admin123"),
            is_admin=True,
        )
        db.add(admin)
        db.commit()
    finally:
        db.close()


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    _bootstrap_admin()
    yield


app = FastAPI(
    title="E-commerce API",
    description="API simples de e-commerce com FastAPI, SQLAlchemy e JWT.",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(api_router)


@app.get("/", tags=["Health"])
def root():
    return {"status": "ok", "service": "ecommerce-api"}
