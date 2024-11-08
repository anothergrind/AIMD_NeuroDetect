from fastapi import FastAPI, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel

app = FastAPI()

# MongoDB connection URI (replace with your MongoDB URI)
MONGO_DB_URI = "mongodb://localhost:27017"
client = AsyncIOMotorClient(MONGO_DB_URI)
db = client.my_database  # Use the database name you want

# Pydantic model to validate data
class Item(BaseModel):
    name: str
    description: str = None

@app.get("/")
async def root():
    return {"message": "Welcome to FastAPI with MongoDB"}

@app.post("/items/", response_model=dict)
async def create_item(item: Item):
    item_dict = item.dict()
    result = await db.my_collection.insert_one(item_dict)
    if result.inserted_id:
        return {"id": str(result.inserted_id), **item_dict}
    raise HTTPException(status_code=500, detail="Item could not be created")

@app.get("/items/")
async def get_items():
    items = await db.my_collection.find().to_list(100)  # Limits to 100 items
    return items
