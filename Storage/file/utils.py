import io
import filetype
from PIL import Image
from fastapi import UploadFile, Request

from Storage.utils import get_api_version

MAX_WIDTH = 1400


async def get_compressed_file(image: UploadFile) -> tuple[bytes | str, str, str]:
    """
    Converts image to png
    """
    content = await image.read()
    kind = filetype.guess(content)
    extension = image.filename.split(".")[-1]
    mime_type = "application/octet-stream"
    if kind is not None:
        mime_type = kind.mime
    # If file is image convert it to webp
    # Because we need to compress images
    # And webp is the best in terms of lossless compression
    # Also need to handle lossless video compression and saving
    if mime_type.startswith("image"):
        img = Image.open(io.BytesIO(content))
        file = io.BytesIO()
        img.save(file, format="webp")
        file.seek(0)
        file = file.read()
        mime_type = "image/webp"
        extension = "webp"
    else:
        file = content
    return file, mime_type, extension


def get_url(request: Request, path: str) -> str:
    """
    Returns URL From Request
    """
    host_name = request.url.hostname
    port = request.url.port
    url = request.url.scheme + "://" + host_name
    if host_name in ["127.0.0.1", "localhost"]:
        url += f":{port}"
    api_prefix = get_api_version()
    url += api_prefix + path
    return url
