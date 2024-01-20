from fastapi import APIRouter
from schema.nftSchema import (
    post_CreateDRM,
    get_Nft,
    patch_NftRights,
    get_nftRightsRequest,
    get_nftSpecificRightsRequest,
    post_UploadMeta,
)
from model.nft import NftModel
from model.rights import rightsModel, giveRightsModel

nft = APIRouter()


@nft.post("/drm/user/askRights/", tags=["nft"], summary="User ask for rights")
def read_root(data: rightsModel):
    """
    ### User ask for rights from admin.
    ### Conditions \n
    merchQuantity: minimum 100 and maximum 1000  \n
    licenseCondition: Copyright,C BY, CC BY-SA, CC BY-NC, CC BY-ND, CC BY-NC-SA, CC BY-NC-ND \n
    licenseTerm: Limited, Perpetuity \n
    licenseCondition: Negotiable, Non-Negotiable \n



    [Documentation Here](https://docs.google.com/document/d/1HKzgolugj8g4oTkMoWPN3gDMprcB9geV7EDAL7MUBOA/edit#heading=h.4fpya9hkk4bs)
    """
    response = post_CreateDRM(data)
    return {"response": response}


@nft.patch(
    "/drm/admin/giveRights/", tags=["nft"], summary="Admin provides rights to users"
)
def read_root(adminId: str, data: giveRightsModel):
    """
    ### Admin give or rights to user.
    ### Condition: Only those rights can be given whose rightsGiven is False \n
    [Documentation Here](https://docs.google.com/document/d/1HKzgolugj8g4oTkMoWPN3gDMprcB9geV7EDAL7MUBOA/edit#heading=h.4fpya9hkk4bs)
    """
    response = patch_NftRights(adminId, data)
    return {"response": response}


@nft.get("/drm/getRights/", tags=["nft"], summary="Get details of Rights Requested")
def read_root():
    """
    ### Admin can get details of all Rights Requested [Documentation Here](https://docs.google.com/document/d/1HKzgolugj8g4oTkMoWPN3gDMprcB9geV7EDAL7MUBOA/edit#heading=h.4fpya9hkk4bs)
    """
    response = get_nftRightsRequest()
    return {"response": response}


@nft.get(
    "/drm/getSpecificRight/",
    tags=["nft"],
    summary="Get details of Specific Rights Requested",
)
def read_root(wallet_id: str):
    """
    ### Admin can get details of Specific Rights Requested by the user from a wallet Id [Documentation Here](https://docs.google.com/document/d/1HKzgolugj8g4oTkMoWPN3gDMprcB9geV7EDAL7MUBOA/edit#heading=h.4fpya9hkk4bs)
    """
    response = get_nftSpecificRightsRequest(wallet_id)
    return {"response": response}


@nft.get("/nft/get/", tags=["nft"], summary="Get NFT")
def read_root(userID):
    """
    ### Get details of NFT [Documentation Here](https://docs.google.com/document/d/1HKzgolugj8g4oTkMoWPN3gDMprcB9geV7EDAL7MUBOA/edit#heading=h.4fpya9hkk4bs)
    """
    response = get_Nft(userID)
    return {"response": response}


@nft.post("/nft/dummy", tags=["nft"], summary="Post meta data of nft")
def read_root(data: NftModel):
    """
    ### User ask for rights from admin.
    ### Conditions \n
    merchQuantity: minimum 100 and maximum 1000  \n
    licenseCondition: Copyright,C BY, CC BY-SA, CC BY-NC, CC BY-ND, CC BY-NC-SA, CC BY-NC-ND \n
    licenseTerm: Limited, Perpetuity \n
    licenseCondition: Negotiable, Non-Negotiable \n



    [Documentation Here](https://docs.google.com/document/d/1HKzgolugj8g4oTkMoWPN3gDMprcB9geV7EDAL7MUBOA/edit#heading=h.4fpya9hkk4bs)
    """
    response = post_UploadMeta(data)
    return {"response": response}
