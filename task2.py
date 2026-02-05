import requests

def fetch_page(url, timeout=10):
    """
    Fetch HTML content from a given URL.

    Args:
        url (str): The URL to fetch
        timeout (int): Request timeout in seconds

    Returns:
        str | None: HTML content if successful, otherwise None
    """
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
    else:
        print("\n[FAILED] Could not fetch the page.")


if __name__ == "__main__":
    main()
