import requests
from bs4 import BeautifulSoup

from shared.db import save_title_as_tag

DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; TimeManagerLabParser/1.0)"
}


def extract_title(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    if soup.title and soup.title.string:
        return soup.title.string.strip()
    return "Untitled page"


def parse_url_and_save(url: str) -> dict:
    response = requests.get(url, timeout=15, headers=DEFAULT_HEADERS)
    response.raise_for_status()

    title = extract_title(response.text)
    saved_id = save_title_as_tag(title)

    return {
        "url": url,
        "title": title,
        "saved_id": saved_id,
        "saved_to": "tag",
    }
