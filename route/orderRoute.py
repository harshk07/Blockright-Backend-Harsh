from fastapi import APIRouter
from schema.orderSchema import post_orderEcommerce, get_allOrder, patch_orderEcommerce
from model.order import OrderModel

order = APIRouter()

@order.post("/order/ecommerce/", tags=['order'], summary="Allow User to Puchase Ecommerce")
def read_root(data: OrderModel):
    """
    ### Allow user to puchase ecommerce
    [Documentation Here](https://docs.google.com/document/d/1HKzgolugj8g4oTkMoWPN3gDMprcB9geV7EDAL7MUBOA/edit#heading=h.4fpya9hkk4bs) 
    """
    response = post_orderEcommerce(data)
    return {"response": response}

@order.get("/order/get/{adminId}", tags=['order'], summary="Allow Admin to Get Order")
def read_root(adminId):
    """
    ### Allow Admin to Get Order 
    ### Condition: \n
    Payment should be done \n
    [Documentation Here](https://docs.google.com/document/d/1HKzgolugj8g4oTkMoWPN3gDMprcB9geV7EDAL7MUBOA/edit#heading=h.4fpya9hkk4bs) 
    """
    response = get_allOrder(adminId)
    return {"response": response}

@order.patch("/order/patch_ecommerce/", tags=['order'], summary="Allow Admin to Update Order")
def read_root(adminId, orderId, data):
    """
    ### Allow Admin to Update Order - orderStatus and orderAmount
    [Documentation Here](https://docs.google.com/document/d/1HKzgolugj8g4oTkMoWPN3gDMprcB9geV7EDAL7MUBOA/edit#heading=h.4fpya9hkk4bs) 
    """
    response = patch_orderEcommerce(adminId,orderId,data)
    return {"response": response}