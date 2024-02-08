from pydantic import BaseModel
from typing import List

class OrderItemModel(BaseModel):
    productImage:str
    price:float
    quantity: int
    color: str
    size: str
    verificationId: str


class OrderModel(BaseModel):
    userId: str
    userName: str
    userEmail: str
    userMobile: int
    city: str
    country: str
    address: str
    pin: int
    products: List[OrderItemModel]
