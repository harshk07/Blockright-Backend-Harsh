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
                "productId": product_data.productId,
                "productTitle": product_data.productTitle,
                "productImg": product_data.productImage,
                "price": product_data.price,
                "quantity": product_data.quantity,
                "size": product_data.size,
                "color": product_data.color,
                "verificationId": product_data.verificationId,
                "totalAmount": product_data.quantity * product_data.price,
            }
            for product_data in data_dict.pop("products")
        ]

        result = order.insert_one(data_dict)
        print(result)

        order_id = str(result.inserted_id)

        total_amount = sum(item["totalAmount"] for item in data_dict["orderedProducts"])

        message = f"Order Pending, Proceed for Payment. Total Amount: {total_amount}"
        return {"order_id": order_id, "Response": message}

    else:
        return "Please enter a 10-digit mobile number"


# def post_orderEcommerce(data):
#     data_dict = dict(data)

#     if len(str(data_dict["userMobile"])) == 10:
#         ordered_products = data_dict.pop("products")
#         total_amount = 0

#         for product_data in ordered_products:
#             product_id = product_data["productId"]
#             ordered_quantity = product_data["quantity"]

#             product = Product.find_one({"_id": ObjectId(product_id)})
#             if product:
#                 available_quantity = Product.get("availableQuantity", 0)
#                 if ordered_quantity <= available_quantity:
#                     total_amount += float(product_data["price"]) * ordered_quantity

#                     # Update available quantity
#                     new_available_quantity = available_quantity - ordered_quantity
#                     Product.update_one(
#                         {"_id": ObjectId(product_id)},
#                         {"$set": {"availableQuantity": new_available_quantity}},
#                     )

#                     # Update ordered product details
#                     product_data["totalAmount"] = (
#                         float(product_data["price"]) * ordered_quantity
#                     )
#                 else:
#                     return f"Insufficient quantity available for product {product_data['merchTitle']}"

#             else:
#                 return f"Product with ID {product_id} not found"

#         # Add additional order details
#         data_dict.update(
#             {
#                 "createdAt": datetime.now(),
#                 "orderStatus": "Pending",
#                 "paymentStatus": "Pending",
#                 "paymentId": None,
#                 "orderedProducts": ordered_products,
#             }
#         )

#         # Insert order into the database
#         order.insert_one(data_dict)

#         return f"Order Pending, Proceed for Payment. Total Amount: {total_amount}"
#     else:
#         return "Please enter a 10-digit mobile number"


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
