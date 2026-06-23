from urllib.parse import urljoin, urlparse
import requests
from bs4 import BeautifulSoup


def get_links(start_url, max_pages=20):
    visited = set()
    urls = []

    try:
        response = requests.get(start_url)
        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        domain = urlparse(start_url).netloc

        for link in soup.find_all("a", href=True):
            href = link["href"]

            absolute_url = urljoin(
                start_url,
                href
            )

            parsed = urlparse(
                absolute_url
            )

            if (
                parsed.netloc == domain
                and
                absolute_url not in visited
            ):
                visited.add(
                    absolute_url
                )
                urls.append(
                    absolute_url
                )

            if len(urls) >= max_pages:
                break

    except Exception as e:
        print(
            f"Crawler Error: {e}"
        )

    return urls