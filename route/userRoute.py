from fastapi import APIRouter
from schema.userSchema import post_userLogin, get_userRights,get_product_detail
from model.user import UserModel, AdminModel

user = APIRouter()

@user.post("/user/login/", tags=['user'], summary="Create User Login")
def create_user_login(data: UserModel):
    """
    ### Add User 
    ### Condition:
    walletType: metamask, coinbase, trust, walletconnect
    [Documentation Here](https://docs.google.com/document/d/1HKzgolugj8g4oTkMoWPN3gDMprcB9geV7EDAL7MUBOA/edit#heading=h.4fpya9hkk4bs) 
    """
    response = post_userLogin(data)
    return {"response": response}

@user.get("/user/getRights/", tags=['user'], summary="Get User Rights")
def get_user_rights(walletId):
    """
    ### Fetch rights that are given to User using user's unique wallet id  [Documentation Here](https://docs.google.com/document/d/1HKzgolugj8g4oTkMoWPN3gDMprcB9geV7EDAL7MUBOA/edit#heading=h.4fpya9hkk4bs) 
    """
    response = get_userRights(walletId)
    # lst = []
    # lst.append(response)
    return response

@user.get("/user/products/{walletId}", tags=['user'], summary="Get Specific Product")
def get_product_details(walletId: str, productId:str ,search: str):
    """
    ### Fetch specific product using user's unique wallet id
    [Documentation Here](https://docs.google.com/document/d/1HKzgolugj8g4oTkMoWPN3gDMprcB9geV7EDAL7MUBOA/edit#heading=h.4fpya9hkk4bs)
    """
    response = get_product_detail(walletId, productId,search)
    return {"response": response}
