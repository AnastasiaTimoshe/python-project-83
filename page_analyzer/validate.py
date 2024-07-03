import validators
from urllib.parse import urlparse


def validate_url(url):
    """Validate url by rules"""
    if not url:
        return 'URL обязателен'
    elif not validators.url(url):
        return 'Некорректный URL'
    else:
        return None


def normalize_url(url):
    """Truncates the URL to the <protocol>://<domain name> structure"""
    try:
        parsed_url = urlparse(url)
        if parsed_url.scheme and parsed_url.netloc:
            url_norm = f"{parsed_url.scheme}://{parsed_url.netloc}"
            return url_norm
        else:
            raise ValueError('Некорректный URL')
    except Exception as e:
        raise ValueError('Некорректный URL') from e
