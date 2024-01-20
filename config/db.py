import pymongo, cloudinary

mongoURI="mongodb://musu:Musu17Hanu@ac-qekgspq-shard-00-00.hrsqgub.mongodb.net:27017,ac-qekgspq-shard-00-01.hrsqgub.mongodb.net:27017,ac-qekgspq-shard-00-02.hrsqgub.mongodb.net:27017/?replicaSet=atlas-gwgnya-shard-0&ssl=true&authSource=admin"
client=pymongo.MongoClient(mongoURI)
x_token_env="1"
orgKey="1"
db=client["blockright"]

user=db["User"]
nft=db["Nft"]
rights=db["Rights"]
admin=db["Admin"]
product=db["Product"]
order=db["Order"]
payment=db["Payment"]

cloudinary.config(
  cloud_name = "dwpjitown",
  api_key = "427843121278645",
  api_secret = "eubGg5OHrF1YmcU4xxcaz2ZQfJU",
  secure = True
)