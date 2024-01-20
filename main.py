from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from route import (
    userRoute,
    nftRoute,
    adminRoute,
    productRoute,
    orderRoute,
    paymentRoute,
)

app = FastAPI(
    title="Blockright",
    description="Mint fashionable NFTs!🚀",
    version="0.0.1",
    docs_url="/api",
    redoc_url="/redoc",
    contact={
        "name": "API Details & Documentation",
        "url": "https://pending.com",
    },
)

# List of allowed origins
origins = [
    "https://example.com",  # Add more allowed origins if needed
    "http://localhost:3000",
    "http://127.0.0.1:8000",  # Replace this with your frontend URL
    "https://blockright.netlify.app",
    "https://open-in-app-zeta.vercel.app",
]

# Include the CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers for different API endpoints
app.include_router(userRoute.user)  # Includes routes defined in userRoute.user
app.include_router(nftRoute.nft)  # Includes routes defined in nftRoute.nft
app.include_router(adminRoute.admin)  # Includes routes defined in adminRoute.admin
app.include_router(
    productRoute.product
)  # Includes routes defined in productRoute.product
app.include_router(orderRoute.order)  # Includes routes defined in orderRoute.order
app.include_router(
    paymentRoute.payment
)  # Includes routes defined in paymentRoute.payment


# Root endpoint
@app.get("/")
def read_root():
    return {"🚀": "BlockRight is Live"}
