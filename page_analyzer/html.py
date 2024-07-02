from bs4 import BeautifulSoup


def extract_page_data(text):
    data = BeautifulSoup(text, "html.parser")
    h1_tag = data.find('h1')
    title_tag = data.find('title')
    meta_description_tag = data.find(
        'meta', attrs={'name': 'description'})
    return {
        'h1': h1_tag.text[:255] if h1_tag else '',
        'title': title_tag.text[:255] if title_tag else '',
        'description': (
            meta_description_tag.get('content', '')[:255]
            if meta_description_tag else '')
    }
