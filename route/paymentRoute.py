from fastapi import APIRouter
from schema.paymentSchema import post_userPayment, patch_adminPayment
from model.payment import PaymentModel

payment = APIRouter()

@payment.post("/payment/make/", tags=['payment'], summary="Make Payment(Pending..)")
def read_root(data: PaymentModel):
    """
    ### Allow user to make make payment for order
    [Documentation Here](https://docs.google.com/document/d/1HKzgolugj8g4oTkMoWPN3gDMprcB9geV7EDAL7MUBOA/edit#heading=h.4fpya9hkk4bs) 
    """
    response = post_userPayment(data)
    return {"response": response}

@payment.patch("/paymtnt/udateOrder/{adminId}/{paymentId}", tags=['payment'], summary="Admin can Update Payment Details(Pending..)")
def read_root(adminId,paymentId,data):
    """
    ### Allow admin to update payment details
    [Documentation Here](https://docs.google.com/document/d/1HKzgolugj8g4oTkMoWPN3gDMprcB9geV7EDAL7MUBOA/edit#heading=h.4fpya9hkk4bs) 
    """
    response = patch_adminPayment(adminId,paymentId,data)
    return {"response": response}