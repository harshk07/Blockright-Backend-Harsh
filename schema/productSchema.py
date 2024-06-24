from bson.objectid import ObjectId
import json
from datetime import datetime, date
import secrets
from model.product import ProductModel
from config.db import *
def post_adminProduct(admin_id: str, data: ProductModel):
    # Convert ProductModel to dictionary
    data_dict = data.dict()

    # Check if admin exists
    if not admin.find_one({"_id": ObjectId(admin_id)}):
        raise HTTPException(status_code=404, detail="Invalid Admin ID")

    # Check if nft and user (walletId) exist
    nft_data = nft.find_one({"_id": ObjectId(data_dict["nftId"])})
    if not nft_data:
        raise HTTPException(status_code=404, detail="Invalid NFT ID")

    wallet_id = user.find_one({"_id": ObjectId(data_dict["walletId"])})
    if not wallet_id:
        raise HTTPException(status_code=404, detail="Invalid Wallet ID")

    # Insert the new product
    result = product.insert_one(data_dict)
    if result.inserted_id:
        product_id = str(result.inserted_id)
    else:
        raise HTTPException(status_code=500, detail="Failed to insert product")

    # Update the product with additional fields
    product.update_one(
        {"_id": ObjectId(product_id)},
        {
            "$set": {
                "walletAddress": nft_data["walletAddress"],
                "isPublished": False,
                "isDeleted": False,
                "drmNumber": secrets.token_hex(8),
            }
        },
    )

    # Update rights document based on nftId
    category = data_dict.get("category", "").lower()
    rights_field = f"{category}Rights"
    rights.update_one(
        {"nftId": data_dict["nftId"]},
        {"$set": {f"{rights_field}.productId": product_id}},
    )

    return "Product added successfully"


def get_allProducts(id):
    from config.db import admin, product, nft

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


def get_product_by_id(product_id):
    # Check if the provided ID is a valid ObjectId
    from config.db import product, admin

    if not product.find_one({"_id": ObjectId(product_id)}):
        raise HTTPException(status_code=400, detail="Invalid product ID")

    product_doc = product.find_one({"_id": ObjectId(product_id)})
    if product_doc:
        # Convert ObjectId to string
        product_doc["_id"] = str(product_doc["_id"])
        return product_doc
    else:
        return None


def patch_products(idA, idP, data):
    from config.db import product, admin, rights

    # Check id admin is there or not
    if admin.find_one({"_id": ObjectId(idA)}):
        # Update value
        # data = json.loads(data)

        # Check if Product is there or not
        document = product.find_one({"_id": ObjectId(idP)})
        if document:
            for field in data.keys():
                if field not in document.keys():
                    return f"Invalid Field: {field}"
                product.update_one({"_id": ObjectId(idP)}, {"$set": dict(data)})
                # rights.update_one({"_id": })
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
