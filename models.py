from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from database import Base

class Product(BaseModel):
    title: str
    asin: str
    amazon_url: str
    affiliate_url: str
    image_url: str | None
    price: str

    def to_model(self):
        return ProductModel(
            title=self.title,
            asin=self.asin,
            amazon_url=self.amazon_url,
            affiliate_url=self.affiliate_url,
            image_url=self.image_url,
            price=self.price,
        )


class ProductModel(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    asin = Column(String)
    amazon_url = Column(String)
    affiliate_url = Column(String)
    image_url = Column(String)
    price = Column(String)
