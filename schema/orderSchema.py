from bson.objectid import ObjectId
import json
from datetime import datetime
import secrets
from model.order import *
from config.db import *


def post_orderEcommerce(data):
    data_dict = dict(data)

    if len(str(data_dict["userMobile"])) == 10:
        data_dict.update(
            {
                "createdAt": datetime.now(),
                "orderStatus": "Pending",
                "paymentStatus": "Pending",
                "paymentId": None,
            }
        )

        # Rename the key to avoid conflicts
        data_dict["orderedProducts"] = [
            {
                "quantity": product_data.quantity,
                "color": product_data.color,
                "size": product_data.size,
                "verificationId": product_data.verificationId,
            }
            for product_data in data_dict.pop("products")
        ]

        order.insert_one(data_dict)

        return "Order Pending, Proceed for Payment"
    else:
        return "Please enter a 10-digit mobile number"


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
