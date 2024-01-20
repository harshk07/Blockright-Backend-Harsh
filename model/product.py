from pydantic import BaseModel
from datetime import datetime

class ProductModel(BaseModel):
    nftId: str
    # walletAddress
    category: str
    originalImage:str
    description:str
    images: list
    tags: list
    price: float
    currency: str= "dollar"
    discount: int
    # isPublished
    totalQuantity: int
    availableQuantity: int
    lastDate: datetime
    merchTitle:str