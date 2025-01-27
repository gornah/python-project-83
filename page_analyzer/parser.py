import requests
from bs4 import BeautifulSoup


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
    response = requests.get(url)
    response.raise_for_status()

    parsed_data = parse_content(response.text)
    return {
        'status_code': response.status_code,
        'h1': parsed_data['h1'],
        'title': parsed_data['title'],
        'description': parsed_data['description']
    }
