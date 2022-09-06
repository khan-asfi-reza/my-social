from Storage.settings import API_PREFIX, API_VERSION


def get_api_version() -> str:
    """
    Returns: API Version with API Prefix
    """
    return f"/{API_PREFIX}/{API_VERSION}"


def route(prefix: str):
    return get_api_version() + prefix
