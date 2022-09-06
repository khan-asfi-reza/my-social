from bson import ObjectId
from motor import motor_asyncio

from Storage.settings import MONGODB_URL

client = motor_asyncio.AsyncIOMotorClient(MONGODB_URL)
db = client.mysocialStorage
storage_collection = db.get_collection("mysocialStorage_collection")


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")
