from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import logging
from typing import Optional
from bson import ObjectId

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MONGO_URL = "mongodb://localhost:27017"
client = AsyncIOMotorClient(MONGO_URL)
db = client["MyProject"]
users_collection = db["users"]

class User(BaseModel):
    user: str
    password: str
    is_user_admin: bool = False
    is_user_manager: bool = False
    is_user_tester: bool = False
    user_timezone: str
    is_user_active: bool = True
    created_at: str = None 

@app.get("/users")
async def get_users():
    document = await users_collection.find_one({})
    
    if not document or "users" not in document:
        return []

    user_list = []
    for user in document["users"]:
        user_list.append({
            "username": user.get("user", "N/A"),
            "password": user.get("password", "N/A"),
            "roles": [
                role for role, has_role in {
                    "admin": user.get("is_user_admin"),
                    "manager": user.get("is_user_manager"),
                    "tester": user.get("is_user_tester"),
                }.items() if has_role
            ],
            "preferences": {"timezone": user.get("user_timezone", "UTC")},
            "active": user.get("is_user_active", True),
            "created_ts": user.get("created_at", "N/A")
        })

    return user_list

def serialize_mongo_doc(document):
    """Converts ObjectId to string in a MongoDB document."""
    if isinstance(document, dict) and "_id" in document:
        document["_id"] = str(document["_id"]) 
    return document

@app.post("/users")
async def create_user(user: User):
    user_dict = {
        "user": user.user,
        "password": user.password,
        "is_user_admin": user.is_user_admin,
        "is_user_manager": user.is_user_manager,
        "is_user_tester": user.is_user_tester,
        "user_timezone": user.user_timezone,
        "is_user_active": user.is_user_active,
        "created_at": user.created_at
    }
    
    main_doc_id = ObjectId("67a67a7c6201e4d31c770fd5")

    result = await users_collection.update_one(
        {"_id": main_doc_id},
        {"$push": {"users": user_dict}} 
    )

    if result.modified_count == 0:
        return {"error": "No document was updated. The ID may be incorrect."}

    return {"message": "User successfully added!", "user": user_dict}

@app.delete("/users/{username}")
async def delete_user(username: str):
    main_doc_id = ObjectId("67a67a7c6201e4d31c770fd5") 

    result = await users_collection.update_one(
        {"_id": main_doc_id},
        {"$pull": {"users": {"user": username}}} 
    )

    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="User not found")

    return {"message": f"User '{username}' delete sucessfully!"}

@app.put("/users/{username}")
async def update_user(username: str, user: User):
    main_doc_id = ObjectId("67a67a7c6201e4d31c770fd5")

    result = await users_collection.update_one(
        {"_id": main_doc_id, "users.user": username},
        {"$set": {
            "users.$.password": user.password,
            "users.$.is_user_admin": user.is_user_admin,
            "users.$.is_user_manager": user.is_user_manager,
            "users.$.is_user_tester": user.is_user_tester,
            "users.$.user_timezone": user.user_timezone,
            "users.$.is_user_active": user.is_user_active,
            "users.$.created_at": user.created_at
        }}
    )

    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="User not found")

    return {"message": f"User '{username}' update sucessfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
