from pymongo import MongoClient

# Connexion MongoDB (en local sur port 27017)
client = MongoClient("mongodb://localhost:27017/")
db = client["articles_db"]
predictions_collection = db["predictions"]
