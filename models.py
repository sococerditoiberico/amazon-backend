from sqlalchemy import Column, Integer, String
from database import Base

class ProductModel(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    asin = Column(String)
    amazon_url = Column(String)
    affiliate_url = Column(String)
    image_url = Column(String)
    price = Column(String)
