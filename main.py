# update

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from models import Product, ProductModel
from database import Base, engine, SessionLocal

# Crear tablas SIN import circular
Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# DB dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def home():
    return {"message": "API funcionando correctamente"}

@app.post("/products")
def create_product(product: Product, db: Session = Depends(get_db)):
    new_product = product.to_model()
    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    backend_url = "https://amazon-backend-47xw.onrender.com"

    return {
        "product_page": f"{backend_url}/product/{new_product.id}"
    }

