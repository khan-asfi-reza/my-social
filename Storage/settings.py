import os
import pathlib

import dotenv

dotenv.load_dotenv()
ROOT_DIR = pathlib.Path(__file__).resolve().parent
STORAGE_DIR = ROOT_DIR / 'store'

API_VERSION = "v1"
API_PREFIX = "api"

CORS_ORIGINS = [
    "http://localhost:8000",
    "http://localhost:9000",
    "http://localhost:3000",
]

MONGODB_URL = os.environ["MONGODB_URL"]
