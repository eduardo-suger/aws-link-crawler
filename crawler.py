import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time

# Starting URL
BASE_URL = "https://docs.aws.amazon.com/marketplace/latest/userguide/what-is-marketplace.html"
DOMAIN = "docs.aws.amazon.com"

# Keep track of visited links
visited = set()
found_links = []

def crawl(url):
    if url in visited:
        return
    visited.add(url)

    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return
    except Exception as e:
        print(f"Error accessing {url}: {e}")
        return

    soup = BeautifulSoup(response.text, "html.parser")
    for link_tag in soup.find_all("a", href=True):
        href = link_tag['href']
        full_url = urljoin(url, href)

        if DOMAIN in urlparse(full_url).netloc and full_url not in visited:
            found_links.append(full_url)
            crawl(full_url)
            time.sleep(0.3)  # gentle delay to avoid hammering the server

# Start crawling
print(f"Starting crawl from: {BASE_URL}")
crawl(BASE_URL)

# Save results
with open("aws_marketplace_links.txt", "w", encoding="utf-8") as f:
    for link in sorted(set(found_links)):
        f.write(link + "\n")

print(f"\nDone. {len(found_links)} links saved to aws_marketplace_links.txt")
