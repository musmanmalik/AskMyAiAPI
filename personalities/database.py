import os
import motor.motor_asyncio
from dotenv import load_dotenv
from fastapi.encoders import jsonable_encoder
from fastapi import Body

from personalities.schema import PersonalitiesSchema, ErrorSchema


# Take environment variables from .env
load_dotenv()

# Connect to the database
mongodb_host = os.environ.get("MONGODB_HOST")
mongodb_url = f"mongodb://{mongodb_host}:27017"

client = motor.motor_asyncio.AsyncIOMotorClient(mongodb_url)

database = client.personalities
personalities_collection = database.get_collection("personalities_collection")
errors_collection = database.get_collection("errors_collection")


# Add a log into to the database
def add_personality(personality: PersonalitiesSchema = Body(...)):
    personality = jsonable_encoder(personality)
    personalities_collection.insert_one(personality)


# Add the error into to the database
def add_error(error: ErrorSchema = Body(...)):
    error = jsonable_encoder(error)
    errors_collection.insert_one(error)

def is_persnality_exist(p_id):
    result = personalities_collection.find({"personality_id": p_id})
        # result is none means employee does not exist.
    if result is None:
        return False
    return True

