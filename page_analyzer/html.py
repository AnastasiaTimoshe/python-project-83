import requests
from bs4 import BeautifulSoup
from datetime import date
from requests.exceptions import RequestException


def html_parser(src):
    soup = BeautifulSoup(src, 'html.parser')
    s_h1 = soup.h1.text if soup.h1 else ''
    s_title = soup.title.text if soup.title else ''
    description = soup.find("meta", attrs={"name": "description"})
    description = description['content'] if description else ''
    return {
        "h1": s_h1,
        "title": s_title,
        "description": description,
    }


def make_check(url, url_id):
    headers = {'user-agent': 'my-app/0.0.1'}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except RequestException as e:
        print(f"Request Exception occurred: {e}")
        return None

    if not response.ok:
        print(f"Request failed with status code: {response.status_code}")
        return None

    src = response.text
    parsing_results = html_parser(src)
    parsing_results["url_id"] = url_id
    parsing_results["status_code"] = response.status_code
    parsing_results["created_at"] = date.today()
    return parsing_results
