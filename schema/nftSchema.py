from bson.objectid import ObjectId
import json
from datetime import datetime, date
import secrets
from model.nft import NftModel
from model.user import *
from model.rights import *
from config.db import *
from fastapi import HTTPException


import secrets


def post_CreateDRM(data):
    data = data.dict()  # Assuming data is a dictionary or object with a dict() method

    # Check for valid user using Wallet ID
    if not user.find_one({"_id": ObjectId(data.get("walletId"))}):
        return "Invalid Wallet ID"

    # Check if NFT is there or not
    if not nft.find_one({"_id": ObjectId(data.get("nftId"))}):
        return "Invalid NFT ID"

    # Checks for user License Condition
    valid_license_conditions = ["Copyright", "C BY", "CC BY-SA"]
    if data.get("userLicenseCondition") not in valid_license_conditions:
        return "Please enter a valid license Condition"

    # Check user license conditions for each category
    categories = ["capRights", "tshirtRights", "hoodieRights", "mugRights"]
    rights_exists = rights.find_one(
        {"walletId": data["walletId"], "nftId": data["nftId"]}
    )

    if rights_exists is not None:
        allocated_categories = []
        for category in categories:
            if data.get(category, {}).get("merchantQuantity", "") == "":
                data[category]["merchantQuantity"] = 0
            if rights_exists.get(category, {}).get("merchantQuantity", "") == "":
                rights_exists[category]["merchantQuantity"] = 0
            if (
                int(data[category]["merchantQuantity"]) > 0
                and int(rights_exists[category]["merchantQuantity"]) > 0
            ):
                allocated_categories.append(category)

        if allocated_categories:
            return f"Rights already allocated for categories: {', '.join(allocated_categories)}"

        for category in categories:
            category_data = data.get(category)
            if not category_data:
                continue

            merch_license_condition = category_data.get("merchLicenseCondition")
            if not merch_license_condition:
                continue

            if merch_license_condition not in ["", "Negotiable", "Non-Negotiable"]:
                return f"Please enter valid {category} Merch license Condition"

            merchant_quantity_str = category_data.get("merchantQuantity", "")
            if merchant_quantity_str:
                merchant_quantity = int(merchant_quantity_str)
                if not (100 <= merchant_quantity <= 1000):
                    return f"Please select quantity between 100 and 1000 for {category}"
            else:
                category_data["merchantQuantity"] = 0

            if int(category_data["merchantQuantity"]) > 0:
                category_data["rightsGiven"] = False

            if rights_exists[category]["merchantQuantity"] == "":
                rights_exists[category] = category_data
            if rights_exists[category]["merchantQuantity"] == 0:
                rights_exists[category] = category_data

        # Update the data into the database
        update_info = rights.update_one(
            {"_id": rights_exists["_id"]}, {"$set": rights_exists}
        ).modified_count
        return f"{update_info} rights req updated"

    # Only insert into the database if at least one category or single data is valid
    any_category_valid = any(
        data.get(category, {}).get("merchLicenseCondition")
        in ["Negotiable", "Non-Negotiable"]
        for category in categories
    )

    if any_category_valid:
        # Insert data into the database
        inserted_id = rights.insert_one(data).inserted_id

        # Update the inserted data
        rights.update_one(
            {"_id": inserted_id},
            {
                "$set": {
                    "capRights.drmNumber": secrets.token_hex(8),
                    "tshirtRights.drmNumber": secrets.token_hex(8),
                    "hoodieRights.drmNumber": secrets.token_hex(8),
                    "mugRights.drmNumber": secrets.token_hex(8),
                    "isAdminVerified": False,
                }
            },
        )

        return "Rights Requested"

    return "Please enter valid data for at least one category or single data"


def get_nftRightsRequest():
    from config.db import rights

    lst = []
    right = rights.find()
    if right:
        for item in right:
            item["_id"] = str(item["_id"])
            lst.append(item)
        return lst
    else:
        return "No Rights"


def get_nftSpecificRightsRequest(wallet_id):
    from config.db import rights

    lst = []
    right = rights.find({"walletId": wallet_id})

    if right:
        # Check capRights
        for eachRight in right:
            capRights = eachRight.get("capRights", {})
            if (
                capRights.get("rightsGiven", False) is False
                and capRights.get("licenseFees", 0) > 0
            ):
                lst.append({"nftId": eachRight.get("nftId"), "capRights": capRights})

            # Check tshirtRights
            tshirtRights = eachRight.get("tshirtRights", {})
            if (
                tshirtRights.get("rightsGiven", False) is False
                and tshirtRights.get("licenseFees", 0) > 0
            ):
                lst.append(
                    {"nftId": eachRight.get("nftId"), "tshirtRights": tshirtRights}
                )

            # Check hoodieRights
            hoodieRights = eachRight.get("hoodieRights", {})
            if (
                hoodieRights.get("rightsGiven", False) is False
                and hoodieRights.get("licenseFees", 0) > 0
            ):
                lst.append(
                    {"nftId": eachRight.get("nftId"), "hoodieRights": hoodieRights}
                )

            # Check mugRights
            mugRights = eachRight.get("mugRights", {})
            if (
                mugRights.get("rightsGiven", False) is False
                and mugRights.get("licenseFees", 0) > 0
            ):
                lst.append({"nftId": eachRight.get("nftId"), "mugRights": mugRights})

        return lst
    else:
        return "You have not requested for any rights yet."


def patch_NftRights(id, data):
    from config.db import rights, user, admin

    data = dict(data)

    # Check Admin is valid using unique id
    if admin.find_one({"_id": ObjectId(id)}):
        # Check if any Rights are there or not
        r = rights.find_one({"_id": ObjectId(data["rightsId"])})
        if r:
            # Check if rights are already given or not
            if r["capRights"]["rightsGiven"] == False:
                rights.update_one(
                    {"_id": ObjectId(data["rightsId"])},
                    {
                        "$set": {
                            "capRights.rightsGiven": data["capRights"]["rightsGiven"]
                        }
                    },
                )
            # else:
            # return "Cap Rights already Given"
            if r["tshirtRights"]["rightsGiven"] == False:
                rights.update_one(
                    {"_id": ObjectId(data["rightsId"])},
                    {
                        "$set": {
                            "tshirtRights.rightsGiven": data["tshirtRights"][
                                "rightsGiven"
                            ]
                        }
                    },
                )
            # else:
            # return "tshirt Rights already Given"
            if r["hoodieRights"]["rightsGiven"] == False:
                rights.update_one(
                    {"_id": ObjectId(data["rightsId"])},
                    {
                        "$set": {
                            "hoodieRights.rightsGiven": data["hoodieRights"][
                                "rightsGiven"
                            ]
                        }
                    },
                )
            # else:
            # return "tshirt Rights already Given"
            if r["mugRights"]["rightsGiven"] == False:
                rights.update_one(
                    {"_id": ObjectId(data["rightsId"])},
                    {
                        "$set": {
                            "mugRights.rightsGiven": data["mugRights"]["rightsGiven"]
                        }
                    },
                )
            # else:
            # return "tshirt Rights already Given"
            rights.update_one(
                {"_id": ObjectId(data["rightsId"])},
                {"$set": {"isAdminVerified": data["isAdminVerified"]}},
            )

            # Code to give Rights
            if data["capRights"]["rightsGiven"] == True:
                rights.update_one(
                    {"_id": ObjectId(data["rightsId"])},
                    {"$set": {"capRights.licenseDate": datetime.now()}},
                )
            if data["tshirtRights"]["rightsGiven"] == True:
                rights.update_one(
                    {"_id": ObjectId(data["rightsId"])},
                    {"$set": {"tshirtRights.licenseDate": datetime.now()}},
                )
            if data["hoodieRights"]["rightsGiven"] == True:
                rights.update_one(
                    {"_id": ObjectId(data["rightsId"])},
                    {"$set": {"hoodieRights.licenseDate": datetime.now()}},
                )
            if data["mugRights"]["rightsGiven"] == True:
                rights.update_one(
                    {"_id": ObjectId(data["rightsId"])},
                    {"$set": {"mugRights.licenseDate": datetime.now()}},
                )
            return "Rights Given"
        else:
            return "Invalid Right ID"
    else:
        return "Invalid Admin"


def get_Nft(userID):
    from config.db import nft

    lst = []
    data = nft.find_one({"userID": userID})
    if data:
        for i in data["nftMetaData"]:
            # i["_id"]=str(i["_id"])
            # i["userID"]=str(i["userID"])

            lst.append(Nft_filter_schema(i))
        return lst
    else:
        return "Invalid NFT ID"


def Nft_filter_schema(item):
    return {
        "name": item["name"],
        "cached_file_url": item["cached_file_url"],
    }


def post_UploadMeta(nft_data):
    # Import your database connection or model here
    from config.db import nft

    try:
        # Convert the Pydantic model instance to a dictionary
        nft_data_dict = nft_data.dict()

        # Insert the NFT metadata into the "nft" collection
        inserted_result = nft.insert_one(nft_data_dict)

        # Check if the insertion was successful
        if inserted_result.acknowledged:
            return "NFT metadata uploaded successfully."
        else:
            return "Failed to upload NFT metadata."
    except Exception as e:
        # Log internal errors
        logging.error(f"Database insertion error: {e}")
        return "Failed to upload NFT metadata."
