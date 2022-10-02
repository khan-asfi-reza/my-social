import requests

from Storage.exceptions import StorageException
from Storage.file.utils import get_url_for_client


def exception_decorator(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except requests.exceptions.HTTPError or requests.exceptions.RequestException:
            raise StorageException("Storage API Request error, please ensure the storage service is working")

    return inner


@exception_decorator
def upload_file(api_endpoint: str, file: str) -> dict[str, str | int]:
    """
    Uploads File to Storage Service
    Args:
        api_endpoint: str, File Storage API Endpoint
        file: File[bytes | bytes array], File to be Uploaded
    """
    url = get_url_for_client(api_endpoint, "upload")
    response = requests.post(url, files={"file": file})
    return response.json()


@exception_decorator
def get_file(api_endpoint: str, file_id: str) -> dict[str, str | int]:
    """
    Get File
    """
    url = get_url_for_client(api_endpoint, file_id)
    response = requests.get(url)
    return response.content


@exception_decorator
def delete_file(api_endpoint: str, file_id: str) -> dict[str, str | int]:
    """
    Deletes File
    """
    url = get_url_for_client(api_endpoint, file_id)
    response = requests.delete(url)
    return response.json()


@exception_decorator
def get_file_details(api_endpoint: str, file_id: str) -> dict[str, str | int]:
    """
    Gets file details
    """
    url = get_url_for_client(api_endpoint, "details", file_id)
    response = requests.get(url)
    data = response.json()
    return data


@exception_decorator
def get_file_details_by_key(api_endpoint: str, file_id: str, key: str, default=None) -> str | int | None:
    """
    Return details field
    """
    details = get_file_details(api_endpoint, file_id)
    return details.get(key, default)


def file_api_url(api_endpoint: str, *args):
    """
    Formats api endpoints
    """
    return get_url_for_client(api_endpoint, *args)
