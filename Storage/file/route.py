import datetime

from bson import ObjectId
from fastapi import routing, File, UploadFile, Request, HTTPException
import aiofiles
from uuid import uuid4

from Storage.file.response import FileResponse

from Storage.db import storage_collection
from Storage.file.models import FileUploadResponse
from Storage.file.utils import get_compressed_file, get_url
from Storage.prefix import FILE_API_PREFIX
from Storage.settings import STORAGE_DIR

router = routing.APIRouter(
    prefix=FILE_API_PREFIX
)


@router.post("/upload", response_model=FileUploadResponse)
async def create_upload_file(request: Request, file: UploadFile = File(...)):
    # Get File Name and extension
    content, mime_type, file_extension, size = await get_compressed_file(file)
    # File Name
    file_name = (
        f"{str(uuid4())}"
        f"{str(uuid4())}"
        "."
        f"{file_extension}"
    )

    # Write file in the system storage
    destination_file_path = STORAGE_DIR / file_name
    async with aiofiles.open(destination_file_path, 'wb') as out_file:
        await out_file.write(content)
    # Generate File Access URL

    db_data = {
        "file_path": file_name,
        "mime_type": mime_type,
        "size": size,
        "created_at": datetime.datetime.now(),
        "updated_at": datetime.datetime.now()
    }
    # Insert data into mongodb
    file = await storage_collection.insert_one(
        db_data
    )
    new_file = await storage_collection.find_one(
        {"_id": ObjectId(file.inserted_id)}
    )
    file_id = str(new_file["_id"])
    url = get_url(request, f"/{file_id}")

    return {
        "status": 201,
        "url": url,
        "id": file_id,
        "mime_type": mime_type,
        "created_at": new_file["created_at"],
        "updated_at": new_file["updated_at"],
        "size": size
    }


@router.get("/details/{file_id}")
async def file_details(file_id: str, request: Request):
    """
    Get File Info
    """
    file = await storage_collection.find_one({"_id": ObjectId(file_id)})
    if file:
        url = get_url(request, f"/file/{file_id}")
        return {
            "status": 201,
            "url": url,
            "id": file_id,
            "mime_type": file["mime_type"],
            "created_at": file["created_at"],
            "updated_at": file["updated_at"],
            "size": file["size"]
        }


@router.get("/{file_id}", response_class=FileResponse)
async def get_file(file_id: str):
    """
    Get File using file id
    """
    file = await storage_collection.find_one({"_id": ObjectId(file_id)})
    if file:
        file_name = file["file_path"]
        destination_file_path = STORAGE_DIR / file_name
        return destination_file_path
    return None


@router.delete("/{file_id}")
async def delete_file(file_id: str):
    """
    Delete file using file id
    """
    file = await storage_collection.find_one({"_id": ObjectId(file_id)})
    if file:
        await storage_collection.delete_one({"_id": ObjectId(file_id)})
        return {
            "status": 203,
            "content": "DELETED"
        }
    raise HTTPException(status_code=404)
