import requests

# Get user input for wallet address and API key
wallet_address = input("Enter wallet address: ")
api_key = "b7fb531b-40ef-4855-bcb0-56ff6374948f"

# Define the API endpoint URL
url = f"https://api.nftport.xyz/v0/accounts/{wallet_address}?chain=polygon"

# Define headers with the Authorization header
headers = {
    "Authorization": api_key,
    "Content-Type": "application/json"
}

# Make a GET request with streaming
response = requests.get(url, headers=headers, stream=True)

# Check if the request was successful
if response.status_code == 200:
    print("Request was successful. Saving response to a file...")
    
    CHUNK_SIZE = 1024  # Adjust the chunk size as needed

    with open("large_response.json", "wb") as file:
        for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
            if chunk:
                file.write(chunk)
    
    print("Response saved to 'large_response.json'. You can process it from there.")
else:
    print(f"Request failed with status code: {response.status_code}")
    print("Response:")
    print(response.text)
