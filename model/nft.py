from pydantic import BaseModel
from datetime import datetime

class NftModel(BaseModel):
    userID: str
    walletAddress: str
    nftMetaData: dict
    rightAllocated: dict ={
        "tshirt":"",
        "cap":"",
        "hoodie":""
    }
    lastSyncedOn: datetime

