import validators
from urllib.parse import urlparse


def validate_url(input_url):
    if not input_url:
        return 'URL обязателен для заполнения'
    if not validators.url(input_url):
        return 'Некорректный URL'
    if len(input_url) > 255:
        return 'Введенный URL превышает длину в 255 символов'


def normalise_url(input_url):
    parsed_url = urlparse(input_url)
    return f"{parsed_url.scheme}://{parsed_url.netloc}"
