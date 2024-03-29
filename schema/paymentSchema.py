from bson import ObjectId
import json
from datetime import datetime
import secrets
from config.db import payment, user, order, product


def post_userPayment(data):
    data_dict = dict(data)
    thatOrder = order.find_one({"_id": ObjectId(data_dict["orderId"])})
    print(thatOrder)

    if thatOrder:
        if thatOrder["paymentStatus"] != "confirmed":
            order.update_one(
                {"_id": ObjectId(data_dict["orderId"])},
                {"$set": {"paymentStatus": "confirmed", "orderStatus": "placed"}},
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
                                "availableQuantity": (
                                    thatProduct["availableQuantity"]
                                    - eachProduct["quantity"]
                                ),
                                "soldQuantity": (
                                    thatProduct["soldQuantity"]
                                    + eachProduct["quantity"]
                                ),
                            }
                        },
                    )
                else:
                    return (
                        "Product with productId: "
                        + str(eachProduct["productId"])
                        + "does not exist"
                    )

            response = (
                "Payment status is set to completed and Order status is set to placed"
            )
            print(response)
            return response
        else:
            return "Payment status is already set to Confirmed"

    else:
        message = "Order does not found with orderId: " + str(data_dict["orderId"])
        return message


def patch_adminPayment(idA, idP, data):
    from config.db import payment, admin, order


def get_transactionDetails(walletAddress):
    allOrders = order.find()
    transactionList = []
    totalEarned = 0
    for eachOrder in allOrders:
        if eachOrder["paymentStatus"] == "confirmed":
            orderEarned = 0
            for eachItem in eachOrder["orderedProducts"]:
                getProductId = eachItem["productId"]
                print("product Id: " + str(getProductId))

                # check if this productId matches with the product document
                # ye product id ko seach karo product collection me aur agar isak walletAddres match kar jay given wallet address se.
                # to selected details ko get karke transaction page me show kar do.

                thatProduct = product.find_one(
                    {"walletAddress": walletAddress, "_id": ObjectId(getProductId)}
                )
                # print(thatProduct)
                if product:
                    transaction_dict = {}
                    # print(eachItem)
                    title = eachItem["productTitle"]
                    category = thatProduct["category"]
                    quantity = eachItem["quantity"]
                    city = eachOrder["city"]
                    address = eachOrder["address"]
                    country = eachOrder["country"]
                    time = eachOrder["createdAt"]
                    price = int(eachItem["price"])
                    totalAmount = price * quantity
                    orderEarned += totalAmount

                    transaction_dict.update(
                        {
                            "title": title,
                            "category": category,
                            "quantity": quantity,
                            "city": city,
                            "address": address,
                            "country": country,
                            "time": time,
                            "price": price,
                            "totalEarned": orderEarned,
                        }
                    )
                    # print(transaction_dict)
                    transactionList.append(transaction_dict)
                totalEarned += orderEarned

    return {"transactionList": transactionList, "earned": totalEarned}
