from bson.objectid import ObjectId
import json
from datetime import datetime, date
from config.db import admin,user,nft

def post_adminSignin(data):
    # data
    # #fullName: str
    # password: str
    # mobile: int
    data = dict(data)
    
    #Check length of mobile number to be 10 digits
    if(len(str(data["mobile"]))==10 ):
            admin.insert_one(data)
            return "Admin added successfully"
    else:
        return "Please enter 10 digit mobile number"
    
def post_adminLogin(mobile,password):
    # from config.db import admin
    
    #Check for mobile number and password
    check=admin.find_one({"mobile":int(mobile)})
    if check:
        if check["password"]==password:
            return "Login Successful"
        else:
            return "Invalid Password"
    else:
        return "Invalid Mobile Number"
    
def admin_dashboard(adminId):
    check=admin.find_one({"_id":ObjectId(adminId)})
    if check:
        users = list(user.find())
        if users ==[]:
            return "No Users found"
        for man in users:
            man["_id"] = str(man["_id"])
        return users
    

def getAllNft(adminId):
    check=admin.find_one({"_id":ObjectId(adminId)})
    if check:
        nfts = list(nft.find())
        if nfts ==[]:
            return "No Users found"
        for man in nfts:
            man["_id"] = str(man["_id"])
        return nfts