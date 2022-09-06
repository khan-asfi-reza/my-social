from datetime import datetime

from bson import ObjectId
from pydantic import BaseModel, Field
from pydantic import root_validator

from Storage.db import PyObjectId


class FileUploadResponse(BaseModel):
    status: str
    url: str
    id: str
    mime_type: str


ImageFileResponse = {
   200: {
       "content": {"image/png": {}}
   }
}


class FileModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    file_path: str = Field(...)
    mime_type: str = Field(...)
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()

    class Config:
        allow_population_by_field_name = True
        validate_assignment = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {"file_id": "d0608943-bd65-40b5-b62c-5ac32662ea1724cde70d-064b-49dd-a7c9-beb127040123",
                        "file_path": "/media/d0608943-bd65-40b5-b62c-5ac32662ea1724cde70d-064b-49dd-a7c9-beb127040123.png"}}

    @root_validator
    def number_validator(cls, values):
        if values["updated_at"]:
            values["updated_at"] = datetime.now()
        else:
            values["updated_at"] = values["created_at"]
        return values
