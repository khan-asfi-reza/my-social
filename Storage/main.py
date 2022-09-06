from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from Storage.file.route import router
from Storage.settings import CORS_ORIGINS
from Storage.utils import get_api_version

app = FastAPI()
prefix = get_api_version()

app.include_router(router, prefix=prefix)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
