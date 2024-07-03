import validators
from urllib.parse import urlparse


def validate_url(url):
    """Validate url by rules"""
    if not url:
        return 'URL обязателен'
    elif not validators.url(url):
        return 'Некорректный URL'


def normalize_url(url):
    """Truncates the URL to the <protocol>://<domain name> structure"""
    url_norm = f"{urlparse(url).scheme}://{urlparse(url).netloc}"
    return url_norm
