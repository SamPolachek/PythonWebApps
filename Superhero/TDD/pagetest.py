from django.urls import Path
from requests import get

urls = Path('urls.txt').read_text()
for url in urls.split('\n'):
    if url:
        print(url, get(url))