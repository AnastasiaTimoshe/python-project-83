import validators
from urllib.parse import urlparse


def validate_url(url):
    if not url:
        return "URL обязателен"
    if len(url) > 255:
        return 'URL не может превышать 255 символов'
    if not validators.url(url):
        return 'Некорректный URL'


def normalize_url(url):
    parsed_url = urlparse(url)
    return f'{parsed_url.scheme}://{parsed_url.netloc}'