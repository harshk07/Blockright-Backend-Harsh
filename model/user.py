from pydantic import BaseModel

class UserModel(BaseModel):
    walletAddress:str
    walletType:str
    totalRefferal: list
    # createdAt
    # nftProcessed
    # nftCollection:list
    # dmActive

class AdminModel(BaseModel):
    fullName: str
    password: str
    mobile: int

class LoginModel(BaseModel):
    mobile: int
    password: str