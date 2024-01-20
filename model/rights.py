from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class rightsModel(BaseModel):
    walletId: str
    nftId: str
    #nftOriginalName: str
    userLicenseCondition: str
    imgSrc: str=""
    capRights: dict={
        "merchantQuantity":0,
        "rightsGiven": False,
        "merchTitle": "",
        "licenseFees": 0.0,
        "merchLicenseCondition": "",
        "licenseTerm": "",
        # "licenseDate": datetime.now(),
        # "expiryDate": datetime.now(),
        # "drmNumber": ""
    }
    tshirtRights: dict={
        "merchantQuantity":0,
        "rightsGiven": False,
        "merchTitle": "",
        "licenseFees": 0.0,
        "merchLicenseCondition": "",
        "licenseTerm": "",
        # "licenseDate": datetime.now(),
        # "expiryDate": datetime.now(),
        # "drmNumber": ""
    }
    hoodieRights:dict={
        "merchantQuantity":0,
        "rightsGiven": False,
        "merchTitle": "",
        "licenseFees": 0.0,
        "merchLicenseCondition": "",
        "licenseTerm": "",
        # "licenseDate": datetime.now(),
        # "expiryDate": datetime.now(),
        # "drmNumber": ""
    }
    mugRights: dict={
        "merchantQuantity":0,
        "rightsGiven": False,
        "merchTitle": "",
        "licenseFees": 0.0,
        "merchLicenseCondition": "",
        "licenseTerm": "",
        # "licenseDate": datetime.now(),
        # "expiryDate": datetime.now(),
        # "drmNumber": ""
    }
    #isAdminVerified: bool
    


class giveRightsModel(BaseModel):
    rightsId: str
    capRights: Optional[dict] = {
        "rightsGiven": False,
        "expiryDate": datetime.now()
    }
    tshirtRights: Optional[dict] = {
        "rightsGiven": False,
        "expiryDate": datetime.now()
    }
    hoodieRights: Optional[dict] = {
        "rightsGiven": False,
        "expiryDate": datetime.now()
    }
    mugRights: Optional[dict] = {
        "rightsGiven": False,
        "expiryDate": datetime.now()
    }
    isAdminVerified: bool
