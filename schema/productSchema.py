from bson.objectid import ObjectId
import json
from datetime import datetime, date
import secrets


def post_adminProduct(id, data):
    from config.db import product, admin, nft, user, rights

    data = dict(data)

    # Check if admin is there or not
    if admin.find_one({"_id": ObjectId(id)}):
        # Check if nft is there or not
        nftData = nft.find_one({"_id": ObjectId(data["nftId"])})
        walletId = user.find_one({"_id": ObjectId(data["walletId"])})

        if nftData and walletId:
            # Insert the new product
            product.insert_one(data)

            # Update the product with additional fields
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

            # Update rights document based on nftId
            nft_id = data.get("nftId")
            category = data.get("category")
            if nft_id and category:
                rights_field = f"{category.lower()}Rights"
                rights.update_one(
                    {"nftId": nft_id},
                    {"$set": {f"{rights_field}.productId": str(data["_id"])}},
                )

            return "Product added successfully"
        else:
            return "Invalid NFT ID"
    else:
        return "Invalid Admin ID"


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
