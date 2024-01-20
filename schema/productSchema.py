from bson.objectid import ObjectId
import json
from datetime import datetime, date
import secrets


def post_adminProduct(id, data):
    from config.db import product, admin, nft

    data = dict(data)

    # Check id admin is there or not
    if admin.find_one({"_id": ObjectId(id)}):
        # Check if nft is there or not
        nftData = nft.find_one({"_id": ObjectId(data["nftId"])})
        if nftData:
            product.insert_one(data)

            product.update_one(
                {"_id": ObjectId(data["_id"])},
                {
                    "$set": {
                        "walletAddress": nftData["walletAddress"],
                        "isPublished": bool(False),
                        "isDeleted": bool(False),
                        "drmNumber": secrets.token_hex(8),
                    }
                },
            )
            return "Product added successfully"

        else:
            return "Invalid NFT ID"
    else:
        return "Invalid Admin ID"


def get_allProducts(id):
    from config.db import admin, product,nft

    lst = []
    # Check id admin is there or not
    if admin.find_one({"_id": ObjectId(id)}):
        # Check if any product is there and get them all
        productData = product.find({})
        if productData:
            for item in productData:
                item["_id"] = str(item["_id"])
                lst.append(item)
            return lst

        else:
            return "No Product found"
    else:
        return "Invalid Admin Id"


def patch_products(idA, idP, data):
    from config.db import product, admin

    # Check id admin is there or not
    if admin.find_one({"_id": ObjectId(idA)}):
        # Update value
        # data = json.loads(data)

        # Check if Product is there or not
        document = product.find_one({"_id": ObjectId(idP)})
        if document:
            # Only certain values can be patched
            # if (
            #     "category" in data
            #     or "images" in data
            #     or "price" in data
            #     or "currency" in data
            #     or "discount" in data
            #     or "isPublished" in data
            #     or "lastDate" in data
            # ):
            for field in data.keys():
                if field not in document.keys():
                    return f"Invalid Field: {field}"
                product.update_one({"_id": ObjectId(idP)}, {"$set": dict(data)})
                return "Product Detail Updated Successfully"

            # else:
            #     return "This field is not Patchable"
        else:
            return "Invalid Product ID"
    else:
        return "Invalid Admin Id"


def delete_products(idA, idP):
    from config.db import product, admin

    # Check id admin is there or not
    if admin.find_one({"_id": ObjectId(idA)}):
        # Check if Product is there or not
        document = product.find_one({"_id": ObjectId(idP)})
        if document:
            product.update_one(
                {"_id": ObjectId(idP)}, {"$set": {"isDeleted": bool(True)}}
            )
            return "Product deleted Successfully"
        else:
            return "Invalid Product ID"
    else:
        return "Invalid Admin Id"
