from pydantic import BaseModel
from typing import List


class OrderItemModel(BaseModel):
    productId: str
    productTitle: str
    productImage: str
    price: float
    quantity: int
    size: str
    color: str
    verificationId: str


class OrderModel(BaseModel):
    userName: str
    userEmail: str
    userMobile: int
    city: str
    country: str
    address: str
    pin: int
    products: List[OrderItemModel]
