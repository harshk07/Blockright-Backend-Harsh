from pydantic import BaseModel


class OrderModel(BaseModel):
    userId: str
    userName: str
    userEmail: str
    userMobile: int
    city: str
    country: str
    actress: str
    pin: int
    
    products: dict ={
        "productImage":"",
        "quantity":0,
        "color":"",
        "size":"",
        "quality":"",
        "verificationId":""
        # printingStatus
    }
    
    # orderAmount: Check
    # orderStatus: Pending
    # paymentStats: Pending
    # paymentID: NULL
