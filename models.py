from sqlmodel import SQLModel, Field
from typing import Optional

class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    asin: str
    amazon_url: str
    affiliate_url: str
    image_url: Optional[str] = None
    price: Optional[str] = None
