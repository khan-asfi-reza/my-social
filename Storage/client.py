import os

import requests
from django.conf import settings
from django.core.files import File
from django.core.files.storage import Storage
from django.utils.deconstruct import deconstructible


def upload_file(file):
    try:
        STORAGE_API = settings.STORAGE_API
        url = STORAGE_API + "/file/upload/"
        response = requests.post(url, files={"file": file})
        return response.json()
    except AttributeError:
        raise Exception("Storage API Not Set in Django Settings")


def get_file(file_id):
    STORAGE_API = settings.STORAGE_API
    url = STORAGE_API + f"/file/{file_id}"
    response = requests.get(url)
    return response.content


@deconstructible
class MySocialStorage(Storage):

    def _open(self, name, mode='rb'):
        file = get_file(name)
        return File(file=file)

    def _save(self, name, content):
        if not hasattr(content, 'seekable') or content.seekable():
            content.seek(0, os.SEEK_SET)
        file = upload_file(content)
        return file["id"]

    def path(self, name):
        STORAGE_API = settings.STORAGE_API
        return STORAGE_API + f"/{name}"

    def delete(self, name):
        pass

    def exists(self, name):
        pass

    def listdir(self, path):
        pass

    def size(self, name):
        return 512

    def url(self, name):
        STORAGE_API = settings.STORAGE_API
        return STORAGE_API + f"/api/{name}"

    def get_accessed_time(self, name):
        pass

    def get_created_time(self, name):
        pass

    def get_modified_time(self, name):
        pass