import hashlib
import os
import stat
from email.utils import formatdate
from mimetypes import guess_type
from urllib.parse import quote

from starlette.exceptions import HTTPException
from starlette.background import BackgroundTask
from fastapi.responses import Response
from starlette.types import Receive, Scope, Send
import aiofiles
from aiofiles.os import stat as aio_stat


class FileResponse(Response):
    chunk_size = 4096

    def __init__(self, path: str, status_code: int = 200, headers: dict = None, media_type: str = None,
                 background: BackgroundTask = None, filename: str = None, stat_result: os.stat_result = None,
                 method: str = None) -> None:

        assert aiofiles is not None, "'aiofiles' must be installed to use FileResponse"
        if filename is None and path is None:
            raise HTTPException(status_code=404, detail="File not found")
        self.path = path
        self.status_code = status_code
        self.filename = filename
        self.send_header_only = method is not None and method.upper() == "HEAD"
        if media_type is None:
            media_type = guess_type(filename or path)[0] or "text/plain"
        self.media_type = media_type
        self.background = background
        self.init_headers(headers)
        if self.filename is not None:
            content_disposition_filename = quote(self.filename)
            if content_disposition_filename != self.filename:
                content_disposition = "attachment; filename*=utf-8''{}".format(
                    content_disposition_filename
                )
            else:
                content_disposition = 'attachment; filename="{}"'.format(self.filename)
            self.headers.setdefault("content-disposition", content_disposition)
        self.stat_result = stat_result
        if stat_result is not None:
            self.set_stat_headers(stat_result)

    def set_stat_headers(self, stat_result: os.stat_result) -> None:
        content_length = str(stat_result.st_size)
        last_modified = formatdate(stat_result.st_mtime, usegmt=True)
        etag_base = str(stat_result.st_mtime) + "-" + str(stat_result.st_size)
        etag = hashlib.md5(etag_base.encode()).hexdigest()

        self.headers.setdefault("content-length", content_length)
        self.headers.setdefault("last-modified", last_modified)
        self.headers.setdefault("etag", etag)

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        try:
            if self.stat_result is None:
                try:
                    stat_result = await aio_stat(self.path)
                    self.set_stat_headers(stat_result)
                except FileNotFoundError:
                    raise RuntimeError(f"File at path {self.path} does not exist.")
                else:
                    mode = stat_result.st_mode
                    if not stat.S_ISREG(mode):
                        raise RuntimeError(f"File at path {self.path} is not a file.")
            await send(
                {
                    "type": "http.response.start",
                    "status": self.status_code,
                    "headers": self.raw_headers,
                }
            )
            if self.send_header_only:
                await send({"type": "http.response.body", "body": b"", "more_body": False})
            else:
                async with aiofiles.open(self.path, mode="rb") as file:
                    more_body = True
                    while more_body:
                        chunk = await file.read(self.chunk_size)
                        more_body = len(chunk) == self.chunk_size
                        await send(
                            {
                                "type": "http.response.body",
                                "body": chunk,
                                "more_body": more_body,
                            }
                        )
            if self.background is not None:
                await self.background()
        except Exception as e:
            print(e)
            raise HTTPException(status_code=404, detail="File not found")


