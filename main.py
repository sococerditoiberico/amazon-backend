from fastapi import FastAPI
from models import Product
from database import engine, SessionLocal
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Depends
from sqlalchemy.orm import Session

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    return {
        "product_page": f"https://TU-DOMINIO/product/{new_product.id}"
    }
