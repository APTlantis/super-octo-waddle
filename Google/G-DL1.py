import json
import os
import requests
import time
import random
from urllib.parse import urlparse, urljoin, parse_qs
from bs4 import BeautifulSoup

# Load dataset links from JSON
with open("google_datasets.json", "r", encoding="utf-8") as f:
    dataset_info = json.load(f)

# Create a folder for downloads
DATASET_DIR = "Datasets"
os.makedirs(DATASET_DIR, exist_ok=True)

# Basic browser headers
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}


def normalize_url(url):
    if not url:
        return None
    url = url.strip()
    # Add scheme for schemeless domains
    if url.startswith("www."):
        url = "https://" + url
    # Resolve protocol-relative
    if url.startswith("//"):
        url = "https:" + url
    # Resolve relative against Google
    if url.startswith("/"):
        url = urljoin("https://www.google.com", url)
    # After initial normalization, unwrap Google redirect /url?q=...
    try:
        pu = urlparse(url)
        if pu.netloc in ("www.google.com", "google.com") and pu.path == "/url":
            qs = parse_qs(pu.query)
            target = qs.get("q", [None])[0]
            if target and target.startswith(("http://", "https://")):
                url = target
    except Exception:
        pass
    # Filter out obvious non-http(s)
    if not (url.startswith("http://") or url.startswith("https://")):
        return None
    # Skip Google login/consent pages
    bad_hosts = {"accounts.google.com", "consent.google.com"}
    try:
        host = urlparse(url).netloc.lower()
        if host in bad_hosts:
            return None
    except Exception:
        return None
    return url


def safe_filename(topic, url, ext=".json"):
    pu = urlparse(url)
    seg = os.path.basename(pu.path) or "index"
    base = f"{topic.replace(' ', '_')}_{pu.netloc}_{seg}"
    # Sanitize
    safe = "".join(ch if ch.isalnum() or ch in ("-", "_", ".", "+") else "_" for ch in base)
    # Limit length and ensure extension
    safe = safe[:195]
    if not safe.endswith(ext):
        safe += ext
    return safe

# Parse dataset JSON-LD from HTML

def parse_dataset_page(html):
    soup = BeautifulSoup(html, "html.parser")
    scripts = soup.find_all("script", type="application/ld+json")
    datasets = []
    for s in scripts:
        try:
            if not s.string:
                continue
            data = json.loads(s.string)
            # Some pages embed arrays of things; normalize to a list
            if isinstance(data, list):
                for item in data:
                    if isinstance(item, dict) and item.get("@type") == "Dataset":
                        datasets.append(item)
            elif isinstance(data, dict) and data.get("@type") == "Dataset":
                datasets.append(data)
        except Exception:
            continue
    return datasets

# Function to download datasets (fetch and parse JSON-LD)

def download_file(url, topic):
    try:
        norm = normalize_url(url)
        if not norm:
            print(f"⏭️ Skipping invalid or unwanted URL: {url}")
            return
        parsed_url = urlparse(norm)
        filename = os.path.join(DATASET_DIR, safe_filename(topic, norm, ext=".json"))

        print(f"⬇️ Downloading: {norm}")
        response = requests.get(norm, headers=HEADERS, timeout=25)
        response.raise_for_status()

        html = response.text
        datasets = parse_dataset_page(html)

        # Save the JSON-LD datasets (even if empty list)
        with open(filename, "w", encoding="utf-8") as f:
            json.dump({
                "topic": topic,
                "source_url": norm,
                "extracted_at": int(time.time()),
                "datasets": datasets,
            }, f, ensure_ascii=False, indent=2)

        if datasets:
            print(f"✅ Saved metadata for {len(datasets)} dataset(s): {filename}\n")
        else:
            print(f"ℹ️ No dataset JSON-LD found; saved placeholder JSON: {filename}\n")

    except Exception as e:
        print(f"❌ Failed to download {url}: {e}")

# Loop through datasets and download files
for topic, datasets in dataset_info.items():
    print(f"\n🔍 Downloading datasets for: {topic}")

    for dataset in datasets:
        dataset_link = dataset.get("link")
        if dataset_link:
            download_file(dataset_link, topic)
            # Randomized delay between requests to reduce rate limiting
            time.sleep(random.uniform(5, 15))

print("\n✅ All possible datasets downloaded!")