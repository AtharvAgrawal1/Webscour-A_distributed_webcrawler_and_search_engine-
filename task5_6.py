import os
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from collections import deque


def fetch_page(url, timeout=10):
    try:
        response = requests.get(
            url,
            timeout=timeout,
            headers={
                "User-Agent": "WebScourBot/1.0 (+https://example.com/bot-info)"
            }
        )
        response.raise_for_status()
        return response.text
    except requests.exceptions.Timeout:
        print(f"[ERROR] Timeout while fetching: {url}")

    except requests.exceptions.HTTPError as e:
        print(f"[ERROR] HTTP error {e.response.status_code} for: {url}")

    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Failed to fetch {url}: {e}")
        return None


def extract_links(html, base_url):
    soup = BeautifulSoup(html, "html.parser")
    links = set()

    for tag in soup.find_all("a", href=True):
        href = tag.get("href").strip()

        if not href or href.startswith(("#", "javascript:", "mailto:", "tel:")):
            continue

        absolute_url = urljoin(base_url, href)
        parsed = urlparse(absolute_url)

        if parsed.scheme in ("http", "https"):
            links.add(absolute_url)

    return links


def save_page(html, page_number):
    os.makedirs("pages", exist_ok=True)
    filename = f"pages/page_{page_number}.html"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(html)

    return filename


def crawl(seed_url, max_pages=10, delay=1):
    queue = deque()
    visited = set()
    page_count = 0

    queue.append(seed_url)

    while queue and page_count < max_pages:
        current_url = queue.popleft()

        if current_url in visited:
            continue

        print(f"Fetching: {current_url}")
        visited.add(current_url)

        html = fetch_page(current_url)
        if not html:
            continue

        page_count += 1
        filename = save_page(html, page_count)

        links = extract_links(html, current_url)

        print(f"Saved: {filename}")
        print(f"Extracted {len(links)} links")

        for link in links:
            if link not in visited and link not in queue :
                queue.append(link)

        time.sleep(delay)

    print("\n[CRAWL COMPLETE]")
    print(f"Total pages saved: {page_count}")
    print(f"Total unique URLs visited: {len(visited)}")



def main():
    seed_url = input("Enter seed URL: ").strip()
    crawl(seed_url, max_pages=10, delay=1)


if __name__ == "__main__":
    main()
