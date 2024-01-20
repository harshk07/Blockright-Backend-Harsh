from fastapi import APIRouter
from schema.adminSchema import post_adminSignin,post_adminLogin,admin_dashboard,getAllNft
# from schema.adminSchema import post_adminLogin
from model.user import *


admin = APIRouter()

@admin.post("/admin/signin/", tags=['admin'], summary="Create Admin Login")
def read_root(data: AdminModel):
    """
    ### Add Admin 
    ### Condition: number must be equal to 10 digits \n
    [Documentation Here](https://docs.google.com/document/d/1HKzgolugj8g4oTkMoWPN3gDMprcB9geV7EDAL7MUBOA/edit#heading=h.4fpya9hkk4bs) 
    """
    response = post_adminSignin(data)
    return {"response": response}

@admin.post("/admin/login", tags=['admin'], summary="Create Admin Login")
async def read_root(data:LoginModel):

    
    """
    ### Login Admin 
    [Documentation Here](https://docs.google.com/document/d/1HKzgolugj8g4oTkMoWPN3gDMprcB9geV7EDAL7MUBOA/edit#heading=h.4fpya9hkk4bs) 
    """
    response = post_adminLogin(data.mobile, data.password)
    return {"response": response}

@admin.get("/admin/getUsers",tags=['admin'])
async def read_root(adminId:str):
    """
    """
    response = admin_dashboard(adminId)
    return response


@admin.get("/admin/getAllNft",tags=['admin'])
async def read_root(adminId:str):
    """
    """
    response = getAllNft(adminId)
    return response
