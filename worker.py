import os
import time
import pika
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def fetch_page(url, timeout=10):
    try:
        response = requests.get(
            url,
            timeout=timeout,
            headers={
                "User-Agent": "WebScourBot/1.0 (+https://example.com/bot-info)"
            },
            verify=False
        )
        response.raise_for_status()
        return response.text
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




visited = set()
page_count = 0
MAX_PAGES = 10


def callback(ch, method, properties, body):
    global page_count

    if page_count >= MAX_PAGES:
        ch.basic_ack(delivery_tag=method.delivery_tag)
        return

    url = body.decode()

    if url in visited:
        ch.basic_ack(delivery_tag=method.delivery_tag)
        return

    print(f"Fetching: {url}")

    html = fetch_page(url)
    if not html:
        ch.basic_ack(delivery_tag=method.delivery_tag)
        return

    visited.add(url)
    page_count += 1

    filename = save_page(html, page_count)
    links = extract_links(html, url)

    print(f"Saved: {filename}")
    print(f"Extracted {len(links)} links")

    
    for link in links:
        if link not in visited:
            ch.basic_publish(
                exchange="",
                routing_key="webscour_queue",
                body=link,
                properties=pika.BasicProperties(
                    delivery_mode=2,
                ),
            )

   
    time.sleep(1)

    ch.basic_ack(delivery_tag=method.delivery_tag)


def main():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="localhost")
    )
    channel = connection.channel()

    channel.queue_declare(queue="webscour_queue", durable=True)

    print("Worker started. Waiting for URLs...")

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(
        queue="webscour_queue",
        on_message_callback=callback
    )

    channel.start_consuming()


if __name__ == "__main__":
    main()
