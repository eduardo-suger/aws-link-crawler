import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, urlunparse
import time

BASE_URL = "https://docs.aws.amazon.com/marketplace/latest/userguide/what-is-marketplace.html"
DOMAIN = "docs.aws.amazon.com"

visited = set()
found_links = []

def clean_url(url):
    parsed = urlparse(url)
    return urlunparse((parsed.scheme, parsed.netloc, parsed.path, '', '', ''))

def crawl(url, depth=0, max_depth=2):
    url = clean_url(url)
    if depth > max_depth or url in visited:
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
    for tag in soup.find_all("a", href=True):
        href = tag['href']
        if any(ext in href for ext in ['.pdf', '.jpg', '.png', '.gif', '.svg', '#']):
            continue
        full_url = urljoin(url, href)
        cleaned = clean_url(full_url)
        if DOMAIN in urlparse(cleaned).netloc and cleaned not in visited:
            found_links.append(cleaned)
            crawl(cleaned, depth + 1, max_depth)
            time.sleep(0.2)  # menor delay

print(f"Starting crawl from: {BASE_URL}")
crawl(BASE_URL)

with open("aws_marketplace_links.txt", "w", encoding="utf-8") as f:
    for link in sorted(set(found_links)):
        f.write(link + "\n")

print(f"\nDone. {len(found_links)} links saved to aws_marketplace_links.txt")

import os
print("\nCurrent directory:", os.getcwd())
print("Files here:", os.listdir())

