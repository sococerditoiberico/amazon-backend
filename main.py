from fastapi import FastAPI, Depends
from sqlmodel import SQLModel, select, Session
from database import engine, get_session
from models import Product

app = FastAPI()

# Crear tablas al iniciar
@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

@app.get("/")
def root():
    return {"status": "API OK"}

@app.post("/products")
def create_product(product: Product, session: Session = Depends(get_session)):
    session.add(product)
    session.commit()
    session.refresh(product)
    
    # Genera URL pública para tu web
    product_link = f"https://TU_WEB.vercel.app/product/{product.id}"
    
    return {
        "ok": True,
        "product_id": product.id,
        "product_page": product_link
    }

@app.get("/products/{product_id}")
def get_product(product_id: int, session: Session = Depends(get_session)):
    statement = select(Product).where(Product.id == product_id)
    result = session.exec(statement).first()
    
    if not result:
        return {"error": "Producto no encontrado"}
    
    return result
