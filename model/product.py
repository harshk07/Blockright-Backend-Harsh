from pydantic import BaseModel
from datetime import datetime


class ProductModel(BaseModel):
    walletId: str
    nftId: str
    category: str
    originalImage: str
    description: str
    images: list
    tags: list
    price: float
    currency: str = "dollar"
    discount: int
    totalQuantity: int
    availableQuantity: int
    soldQuantity: int
    lastDate: datetime
    merchTitle: str
