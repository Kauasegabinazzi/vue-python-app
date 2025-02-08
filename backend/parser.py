import json
from pymongo import MongoClient
from bson import ObjectId 

client = MongoClient("mongodb://localhost:27017/")
db = client["MyProject"] 
collection = db["users"] 

user_id = "67a67a7c6201e4d31c770fd5"

with open("users.json", "r", encoding="utf-8") as file:
    user_data = json.load(file)

result = collection.update_one(
    {"_id": ObjectId(user_id)},
    {"$set": user_data} 
)

# Verifica se foi atualizado
if result.matched_count > 0:
    print("✅ User successfully updated!")
else:
    print("⚠️ No user found with this ID.")
