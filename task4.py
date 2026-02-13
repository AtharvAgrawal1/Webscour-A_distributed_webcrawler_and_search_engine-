import requests
from collections import deque
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def crawl(seed_url, max_pages=10):
    queue = deque()
    visited = set()

    queue.append(seed_url)

    while queue and len(visited) < max_pages:
        current_url = queue.popleft()

        if current_url in visited:
            continue

        print(f"\n[CRAWLING] {current_url}")
        visited.add(current_url)

        html = fetch_page(current_url)
        if not html:
            continue

        links = extract_links(html, current_url)

        for link in links:
            if link not in visited:
                queue.append(link)

    print("\n[CRAWL COMPLETE]")
    print(f"Total pages visited: {len(visited)}")

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
        print(f"[ERROR] Request failed for {url}: {e}")

    return None


def main():
    url = input("Enter URL to fetch: ").strip()
    html = fetch_page(url)

    if html:
        print("\n[SUCCESS] Page fetched successfully!")
        print(f"HTML length: {len(html)} characters\n")
        print(html[:1000])  
        links = extract_links(html, url)
        print(f"Found {len(links)} links:\n")
        for link in list(links)[:10]:
            print(link)
        crawl(url)

    else:
        print("\n[FAILED] Could not fetch the page.")


if __name__ == "__main__":
    main()