import requests
from bs4 import BeautifulSoup


def parse_url(url_name):
    url_response = requests.get(url_name)
    url_response.raise_for_status()
    soup = BeautifulSoup(url_response.text, 'html.parser')
    status_code = url_response.status_code
    h1 = soup.h1.string if soup.h1 else ''
    title = soup.find('title').string if soup.find('title') else ''
    all_meta_tags = soup.find_all("meta")
    description = ""
    for meta_tag in all_meta_tags:
        if meta_tag.get("name") == "description":
            description = meta_tag.get('content')
            break
    return status_code, h1, title, description
