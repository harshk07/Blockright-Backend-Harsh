from bson.objectid import ObjectId
import json
from datetime import datetime
import secrets

def post_orderEcommerce(data):
    from config.db import order, user, product
    data = dict(data)
    
    #Check User ID 
    if user.find_one({"_id":ObjectId(data["userId"])}):
        
        #Check length of mobile number to be 10 digits
        if(len(str(data["userMobile"]))==10 ):
        
        #Calculations
        #TODO
        # prod=product.find({})
        # for item1 in prod:
        #     for item2 in range(0:(data["product"]).len()):
        #         if item1["images"]==item2["product"]["productImage"]:
        #             c=prod["price"]*item2["product"]["quantity"]
        #             d=c*prod["discount"]
        #             sum=sum+(c-d)
        

            order.insert_one(data)

            order.update_one({"_id": data["_id"]}, {"$set": {"createdAt": datetime.now(),
                                                    "orderAmount": bool(False),
                                                    "products.orderStatus": str("Pending"),
                                                    "paymentStatus": str("Pending"),
                                                    "paymentId": None
                                                    }})
            return "Order Pending, Proceed for Payment"
        else:
            return "Please enter 10 digit mobile number"
    else:
        return "Invalid User Id"
    
def get_allOrder(id):
    from config.db import order, admin
    lst = []
    orderData = order.find({})
    
    # Check if Admin is valid or not
    admin_data = admin.find_one({"_id": ObjectId(id)})
    if admin_data:
        
        for item in orderData:
                
            # Check if payment is done
            if item["paymentStatus"] != "Pending":
                item["_id"] = str(item["_id"])
                lst.append(item)
        return lst
    else:
        return "Invalid Admin ID"
    
def patch_orderEcommerce(idA, idO, data):
    from config.db import order, admin
    data = json.loads(data)

    # Check if Admin is valid or not
    admin_data = admin.find_one({"_id": ObjectId(idA)})
    if admin_data:

        # Check if Order is there or not
        document = order.find_one({"_id": ObjectId(idO)})
        if document:

            # Only certain values can be patched
            if "products.orderStatus" in data or "orderAmount" in data:
                order.update_one({"_id": ObjectId(idO)}, {"$set": data})
                return "Order Detail Updated Successfully"
            
            else:
                return "This field is not Patchable"
        else:
            return "Invalid Order ID"
    else:
        return "Invalid Admin Id"

    