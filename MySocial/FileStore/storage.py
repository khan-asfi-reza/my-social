import datetime

from cryptography.fernet import Fernet
from django.conf import settings
from django.core.files import File
from django.core.files.storage import Storage
from django.utils.deconstruct import deconstructible
import json

from Storage.client import get_file, upload_file, delete_file, file_api_url


@deconstructible
class MySocialMediaStorage(Storage):
    """
    This storage service, uses the MySocial Storage API
    While uploading any file the file returns json response
    the required data are converted into bytes and which is later converted to
    an encrypted string
    """
    def __init__(self):
        try:
            # Import API Endpoints from settings
            self.STORAGE_API = settings.STORAGE_API
            self.STORAGE_SECRET = settings.STORAGE_SECRET
            # Encryption Fernet
            self.fernet = Fernet(self.STORAGE_SECRET)
        except AttributeError or ImportError:
            raise Exception("STORAGE_API and STORAGE_SECRET must be initiated in the settings file")
        super(MySocialMediaStorage, self).__init__()

    def _open(self, name, mode="rb"):
        file_id = self._get_file_object(name).get("id")
        return File(get_file(self.STORAGE_API, file_id))

    def _save(self, name, content):
        file = upload_file(self.STORAGE_API, content)
        file = {
            "id": file["id"],
            "size": file["size"],
            "created_at": file["created_at"],
            "uploaded_at": file["updated_at"]
        }
        json_string = json.dumps(file).encode('utf-8')
        return self.fernet.encrypt(json_string).decode('utf-8')

    def _get_file_object(self, name):
        # Decrypt and return file object
        decrypted = self.fernet.decrypt(name)
        return json.loads(decrypted)

    def delete(self, name):
        delete_file(self.STORAGE_API, name)

    def exists(self, name):
        return False

    def listdir(self, path):
        return []

    def path(self, name):
        name = self._get_file_object(name).get("id")
        return file_api_url(self.STORAGE_API, name)

    def size(self, name):
        return self._get_file_object(name).get("size", None)

    def url(self, name):
        name = self._get_file_object(name).get("id")
        return file_api_url(self.STORAGE_API, name)

    def get_accessed_time(self, name):
        return datetime.datetime.now()

    def get_created_time(self, name):
        return self._get_file_object(name).get("created_at", None)

    def get_modified_time(self, name):
        return self._get_file_object(name).get("updated_at", None)
