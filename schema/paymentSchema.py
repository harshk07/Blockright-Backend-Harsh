from bson.objectid import ObjectId
import json
from datetime import datetime
import secrets
from config.db import payment, user, order, product


def post_userPayment(data):
    data_dict = dict(data)
    thatOrder = order.find_one({"_id": ObjectId(data_dict["orderId"])})
    print(thatOrder)

    if thatOrder:
        if thatOrder["paymentStatus"] is not "completed":
            order.update_one(
                {"_id": ObjectId(data_dict["orderId"])},
                {"$set": {"paymentStatus": "completed"}},
            )

            for eachProduct in thatOrder["orderedProducts"]:
                thatProduct = product.find_one(
                    {"_id": ObjectId(eachProduct["productId"])}
                )

                if thatProduct:
                    product.update_one(
                        {"_id": ObjectId(eachProduct["productId"])},
                        {
                            "$set": {
                                "totalQuantity": (
                                    thatProduct["totalQuantity"]
                                    - eachProduct["quantity"]
                                )
                            }
                        },
                    )
                else:
                    return (
                        "Product with productId: "
                        + str(eachProduct["productId"])
                        + "does not exist"
                    )

            response = "Payment status is set to completed"
            print(response)
            return response
        else:
            return "Payment status is already set to completed"

    else:
        message = "Order does not found with orderId: " + str(data_dict["orderId"])
        return message


def patch_adminPayment(idA, idP, data):
    from config.db import payment, admin, order
