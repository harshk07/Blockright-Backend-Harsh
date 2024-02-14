from fastapi import APIRouter
from schema.productSchema import (
    post_adminProduct,
    get_allProducts,
    patch_products,
    delete_products,
    get_product_by_id,
)
from model.product import ProductModel

product = APIRouter()


@product.post("/ecommerce/add/", tags=["product"], summary="Add new product by Admin")
def read_root(adminId: str, data: ProductModel):
    """
    ### Add new product by the Admin
    [Documentation Here](https://docs.google.com/document/d/1HKzgolugj8g4oTkMoWPN3gDMprcB9geV7EDAL7MUBOA/edit#heading=h.4fpya9hkk4bs)
    """
    response = post_adminProduct(adminId, data)
    return {"response": response}


@product.get(
    "/ecommerce/getAll/", tags=["product"], summary="View all products to admin"
)
def read_root(adminId: str):
    """
    ### View all products to admin
    [Documentation Here](https://docs.google.com/document/d/1HKzgolugj8g4oTkMoWPN3gDMprcB9geV7EDAL7MUBOA/edit#heading=h.4fpya9hkk4bs)
    """
    response = get_allProducts(adminId)
    return {"response": response}


@product.get(
    "/ecommerce/getSpecificProduct/{product_id}",
    tags=["product"],
    summary="View a specific product",
)
def get_product(product_id: str):
    """
    ### View a specific product
    [Documentation Here](https://docs.google.com/document/d/1HKzgolugj8g4oTkMoWPN3gDMprcB9geV7EDAL7MUBOA/edit#heading=h.4fpya9hkk4bs)
    """
    product_doc = get_product_by_id(product_id)
    if product_doc:
        return product_doc
    else:
        raise HTTPException(status_code=404, detail="Product not found")


@product.patch(
    "/ecommerce/editDetails/", tags=["product"], summary="Patch product details"
)
def read_root(adminId: str, productId: str, data: dict):
    """
    ### Update product details
    [Documentation Here](https://docs.google.com/document/d/1HKzgolugj8g4oTkMoWPN3gDMprcB9geV7EDAL7MUBOA/edit#heading=h.4fpya9hkk4bs)
    """
    response = patch_products(adminId, productId, data)
    return {"response": response}


@product.delete(
    "/ecommerce/productDelete/{adminId}/{productId}",
    tags=["product"],
    summary="Delete Product",
)
def read_root(adminId, productId):
    """
    ### Soft detlete product
    [Documentation Here](https://docs.google.com/document/d/1HKzgolugj8g4oTkMoWPN3gDMprcB9geV7EDAL7MUBOA/edit#heading=h.4fpya9hkk4bs)
    """
    response = delete_products(adminId, productId)
    return {"response": response}
