from bson.objectid import ObjectId
import json
import requests
from datetime import datetime, date
import secrets
from config.db import payment, user, order, product,nft
from fastapi import HTTPException
# def post_userLogin(data):
#     from config.db import user, nft

#     data = dict(data)

#     allowed_wallet_types = ["metamask", "coinbase", "trust wallet", "wallet connect"]
#     if data["walletType"].lower() in allowed_wallet_types:
#         user.insert_one(data)

#         user.update_one({"_id": data["_id"]}, {"$set": {
#             "createdAt": datetime.now(),
#             "nftProcessed": False,
#             "dmActive": False,
#             "nftCollection": [],
#             "refferaID": secrets.token_hex(6)
#         }})

#         nft_data = {
#             "userID": str(data["_id"]),
#             "walletAddress": data["walletAddress"],
#             "nftMetaData": "",
#             "rightAllocated": {
#                 "tshirt": None,
#                 "cap": None,
#                 "hoodie": None,
#                 "cup": None
#             },
#             "lastSyncedOn": None,
#             "isOwned": True,
#             "isAdminVerified": False
#         }
#         nft.insert_one(nft_data)

#         message = "Login Created Successfully"
#         user_id = str(data["_id"])
#         response = {"message": message, "walletId": user_id}
#         return response
#     else:
#         return "Invalid Wallet Type"


def post_userLogin(data):
    # Define the API endpoint URL and API key
    api_key = "krishnacool7_sk_y7r7ni208up5sd16h6987i2gs1w5zurc"
    url = f"https://api.simplehash.com/api/v0/nfts/owners?chains=polygon,ethereum&wallet_addresses={data.walletAddress}&limit=50"

    # Define headers with the Authorization header
    headers = {
        "accept": "application/json",
        "X-API-KEY": api_key,
    }

    # Make a GET request with streaming
    response = requests.get(url, headers=headers, stream=True)
    if response.status_code == 200:
        nftResponse = response.json()
        Nfts = nftResponse.get("nfts", [])
    else:
        response.raise_for_status()

    # Convert data to dictionary if it's not already
    if not isinstance(data, dict):
        data = data.dict()

    # Check if a user with the same wallet address already exists
    existing_user = user.find_one({"walletAddress": data["walletAddress"]})

    if existing_user:
        # User already exists, update the number of NFTs
        num_nfts = len(Nfts)
        user.update_one(
            {"walletAddress": data["walletAddress"]},
            {"$set": {"numberOfNfts": num_nfts}}
        )

        # Return an appropriate response
        message = "User already exists"
        user_id = str(existing_user["_id"])
        nft_data = nft.find_one({"userID": user_id})
        nft_id = str(nft_data["_id"]) if nft_data else None
        response = {"message": message, "walletId": user_id, "nftId": nft_id}
        return response

    allowed_wallet_types = ["metamask", "coinbase", "trust wallet", "wallet connect"]
    if data["walletType"].lower() in allowed_wallet_types:
        new_user = {
            "createdAt": datetime.now(),
            "nftProcessed": False,
            "dmActive": False,
            "refferaID": secrets.token_hex(6),
            "numberOfNfts": len(Nfts),  # Add the number of NFTs
        }
        data.update(new_user)
        user_id = user.insert_one(data).inserted_id

        nft_ids = []
        for nft_metadata in Nfts:
            if nft_metadata.get("image_url") is not None:
                nft_doc = {
                    "userID": str(user_id),
                    "walletAddress": data["walletAddress"],
                    "nftMetaData": nft_metadata,
                    "rightAllocated": {
                        "tshirt": None,
                        "cap": None,
                        "hoodie": None,
                        "cup": None,
                    },
                    "lastSyncedOn": None,
                    "isOwned": True,
                    "isAdminVerified": False,
                }
                nft_id = nft.insert_one(nft_doc).inserted_id
                nft_ids.append(str(nft_id))

        response = {"message": "Login Created Successfully", "walletId": str(user_id), "nftIds": nft_ids}
        return response
    else:
        raise HTTPException(status_code=400, detail="Invalid Wallet Type")


def get_userRights(id):
    from config.db import rights

    user_data_cursor = rights.find({"walletId": str(id)})
    user_rights_list = []

    for user_data in user_data_cursor:
        wallet = user_data["walletId"]
        userLicense_condition = user_data["userLicenseCondition"]
        nft_id = user_data["nftId"]

        # Initialize variables inside the loop
        cap_info = {}
        tshirt_info = {}
        hoodie_info = {}
        mug_info = {}

        cap_rights = user_data.get("capRights", {})
        tshirt_rights = user_data.get("tshirtRights", {})
        hoodie_rights = user_data.get("hoodieRights", {})
        mug_rights = user_data.get("mugRights", {})

        cap_rights_given = cap_rights.get("rightsGiven", False)
        tshirt_rights_given = tshirt_rights.get("rightsGiven", False)
        hoodie_rights_given = hoodie_rights.get("rightsGiven", False)
        mug_rights_given = mug_rights.get("rightsGiven", False)

        # Update the variables only if corresponding data is available
        print("Hello")
        if cap_rights_given:
            AvailableQuantity = product.find_one(
                {"nftId": str(nft_id), "category": "cap"}
            )
            if not AvailableQuantity:
                AvailableQuantity = {}
            # capAvailableQuantity["_id"] = str(capAvailableQuantity["_id"])
            # print(capAvailableQuantity)
            cap_info = {
                "merchantQuantity": cap_rights.get("merchantQuantity", 0),
                "merchTitle": cap_rights.get("merchTitle", ""),
                "licenseFees": cap_rights.get("licenseFees", 0),
                "merchLicenseCondition": cap_rights.get("merchLicenseCondition", ""),
                "licenseTerm": cap_rights.get("licenseTerm", ""),
                "licenseDate": cap_rights.get("licenseDate", ""),
                "productId": cap_rights.get("productId", ""),
                "availableQuantity": AvailableQuantity.get("availableQuantity"),
                "soldQuantity": AvailableQuantity.get("soldQuantity", 0),
            }

        if tshirt_rights_given:
            AvailableQuantity = product.find_one(
                {"nftId": str(nft_id), "category": "tshirt"}
            )
            if not AvailableQuantity:
                AvailableQuantity = {}
            tshirt_info = {
                "merchantQuantity": tshirt_rights.get("merchantQuantity", 0),
                "merchTitle": tshirt_rights.get("merchTitle", ""),
                "licenseFees": tshirt_rights.get("licenseFees", 0),
                "merchLicenseCondition": tshirt_rights.get("merchLicenseCondition", ""),
                "licenseTerm": tshirt_rights.get("licenseTerm", ""),
                "licenseDate": tshirt_rights.get("licenseDate", ""),
                "productId": tshirt_rights.get("productId", ""),
                "availableQuantity": AvailableQuantity.get("availableQuantity"),
                "soldQuantity": AvailableQuantity.get("soldQuantity", 0),
            }

        if hoodie_rights_given:
            AvailableQuantity = product.find_one(
                {"nftId": str(nft_id), "category": "hoodie"}
            )
            if not AvailableQuantity:
                AvailableQuantity = {}
            hoodie_info = {
                "merchantQuantity": hoodie_rights.get("merchantQuantity", 0),
                "merchTitle": hoodie_rights.get("merchTitle", ""),
                "licenseFees": hoodie_rights.get("licenseFees", 0),
                "merchLicenseCondition": hoodie_rights.get("merchLicenseCondition", ""),
                "licenseTerm": hoodie_rights.get("licenseTerm", ""),
                "licenseDate": hoodie_rights.get("licenseDate", ""),
                "productId": hoodie_rights.get("productId", ""),
                "availableQuantity": AvailableQuantity.get("availableQuantity"),
                "soldQuantity": AvailableQuantity.get("soldQuantity", 0),
            }

        if mug_rights_given:
            AvailableQuantity = product.find_one(
                {"nftId": str(nft_id), "category": "mug"}
            )
            if not AvailableQuantity:
                AvailableQuantity = {}
            mug_info = {
                "merchantQuantity": mug_rights.get("merchantQuantity", 0),
                "merchTitle": mug_rights.get("merchTitle", ""),
                "licenseFees": mug_rights.get("licenseFees", 0),
                "merchLicenseCondition": mug_rights.get("merchLicenseCondition", ""),
                "licenseTerm": mug_rights.get("licenseTerm", ""),
                "licenseDate": mug_rights.get("licenseDate", ""),
                "productId": mug_rights.get("productId", ""),
                "availableQuantity": AvailableQuantity.get("availableQuantity"),
                "soldQuantity": AvailableQuantity.get("soldQuantity", 0),
            }

        user_rights = {
            "walletId": wallet,
            "userLicenseCondition": userLicense_condition,
            "nftId": nft_id,
            "imgSrc": user_data["imgSrc"],
            "capRights": cap_info,
            "tshirtRights": tshirt_info,
            "hoodieRights": hoodie_info,
            "mugRights": mug_info,
        }

        # Append user rights only if at least one right is given
        if any(
            [
                cap_rights_given,
                tshirt_rights_given,
                hoodie_rights_given,
                mug_rights_given,
            ]
        ):
            user_rights_list.append(user_rights)

    if len(user_rights_list) == 0:
        return {"message": "No rights approved"}
    else:
        return user_rights_list


def get_product_detail(id, prod, search):
    from config.db import user, product

    user_data = user.find_one({"walletAddress": str(id)})
    if user_data:
        data = product.find_one({"_id": ObjectId(prod)})
        if data:
            tags = data["tags"]
            category = data["category"]

            if search in tags or search in category:  # Updated this line
                if data["isPublished"] and not data["isDeleted"]:
                    nft_id = data["nftId"]
                    cat = data["category"]
                    img = data["images"]
                    tag = data["tags"]
                    price = data["price"]
                    currency = data["currency"]
                    discount = data["discount"]
                    available = data["availableQuantity"]
                    last_date = data["lastDate"]

                    response = {
                        "nftId": nft_id,
                        "category": cat,
                        "images": img,
                        "tags": tag,
                        "price": price,
                        "currency": currency,
                        "discount": discount,
                        "availableQuantity": available,
                        "lastDate": last_date,
                    }
                    return response
                else:
                    return "Product is not published or deleted"
            else:
                return "No Keyword found"
        else:
            return "Product not found"
    else:
        return "Invalid Wallet Id"
