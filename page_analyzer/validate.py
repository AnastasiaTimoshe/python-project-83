import validators
from urllib.parse import urlparse


def validate(url):
    url_validator = validators.url(url)
    if not url:
        return 'URL обязателен для заполнения'
    if not url_validator:
        return 'Некорректный URL'
    if len(url) > 255:
        return 'URL слишком длинный'


def normalize_url(url):
    parsed_url = urlparse(url)
    normalized_scheme = parsed_url.scheme.lower()
    normalized_host = parsed_url.hostname.lower()
    return f'{normalized_scheme}://{normalized_host}'
