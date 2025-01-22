import validators
import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup


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


def parse_content(content: str) -> dict:
    """
    Parses the HTML content to extract H1, title, and description.
    """
    soup = BeautifulSoup(content, 'html.parser')
    h1 = soup.find('h1')
    title = soup.find('title')
    description = soup.find('meta', attrs={'name': 'description'})

    return {
        'h1': h1.text.strip() if h1 else '',
        'title': title.text.strip() if title else '',
        'description': (
            description['content'].strip()
            if description and 'content' in description.attrs
            else ''
            )
    }


def get_check_data(url: str) -> dict:
    """
    Fetches the URL content, parses it, and returns relevant metadata.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise Exception(f"Ошибка при запросе к {url}: {e}")

    parsed_data = parse_content(response.text)
    return {
        'status_code': response.status_code,
        'h1': parsed_data['h1'],
        'title': parsed_data['title'],
        'description': parsed_data['description']
    }
