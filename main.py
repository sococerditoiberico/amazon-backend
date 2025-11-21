from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import requests
from bs4 import BeautifulSoup

from models import ProductModel
from database import Base, engine, SessionLocal

Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def home():
    return {"message": "API funcionando correctamente"}

# SCRAPING EN EL BACKEND
def scrape_amazon(asin: str):
    url = f"https://www.amazon.es/dp/{asin}"
    headers = {"User-Agent": "Mozilla/5.0"}

    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        return None

    soup = BeautifulSoup(r.text, "html.parser")

    title = soup.find(id="productTitle")
    title = title.get_text(strip=True) if title else "Producto Amazon"

    img = soup.find(id="landingImage")
    image_url = img.get("src") if img else None

    price_tag = soup.find(id="priceblock_ourprice") or soup.find(id="priceblock_dealprice")
    price = price_tag.get_text(strip=True) if price_tag else "No disponible"

    affiliate = f"https://www.amazon.es/dp/{asin}/?tag=crdt25-21"

    return {
        "title": title,
        "asin": asin,
        "amazon_url": url,
        "affiliate_url": affiliate,
        "image_url": image_url,
        "price": price,
    }

@app.post("/products")
def create_product(data: dict, db: Session = Depends(get_db)):

    asin = data.get("asin")
    if not asin:
        return {"error": "ASIN requerido"}

    scraped = scrape_amazon(asin)
    if scraped is None:
        return {"error": "Scraping falló"}

    new = ProductModel(**scraped)
    db.add(new)
    db.commit()
    db.refresh(new)

    backend_url = "https://amazon-backend-iy2x.onrender.com"

    return {
        "product_page": f"{backend_url}/product/{new.id}"
    }
