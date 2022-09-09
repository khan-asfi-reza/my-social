import requests
from django.conf import settings


def upload_file(file):
    try:
        STORAGE_API = settings.STORAGE_API
        url = STORAGE_API + "/upload"
        response = requests.post(url, files={"file": file})
        return response.json()
    except AttributeError:
        raise Exception("Storage API Not Set in Django Settings")

