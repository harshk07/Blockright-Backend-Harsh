from pydantic import BaseModel

class PaymentModel(BaseModel):
    userId: str
    orderId: str
    amount: float