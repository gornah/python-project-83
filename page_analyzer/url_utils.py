from urllib.parse import urlparse

import validators


def validate(url: str) -> list:
    """
    Validates the given URL for correctness and length.
    Returns a list of error messages or an empty list if valid.
    """
    errors = []
    if not url:
        errors.append('URL обязателен')
    elif not validators.url(url):
        errors.append('Некорректный URL')
    elif len(url) > 255:
        errors.append('URL превышает 255 символов')
    return errors


def normalize_url(url: str) -> str:
    """
    Normalizes a URL to retain only the scheme and host.

    Example:
    normalize_url("https://www.example.com/some/path?query=param#fragment")
    will return "https://www.example.com".
    """
    parsed_url = urlparse(url)
    if not parsed_url.scheme or not parsed_url.hostname:
        return ""
    return f"{parsed_url.scheme}://{parsed_url.hostname}"
