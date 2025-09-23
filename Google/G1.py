import requests
from bs4 import BeautifulSoup
import json
import time
import random

# Load structured search topics JSON
TOPIC_JSON_FILE = "search_topics.json"

# Google SERP with site filter to Dataset Search results
GOOGLE_SEARCH_URL = "https://www.google.com/search?q=site%3Adatasetsearch.research.google.com+{}&num=10&hl=en"

# Headers to pretend we're a real browser
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}

def _extract_topics(data):
    topics = []
    if isinstance(data, list):
        for item in data:
            if isinstance(item, str):
                topics.append(item)
            else:
                topics.extend(_extract_topics(item))
    elif isinstance(data, dict):
        for value in data.values():
            topics.extend(_extract_topics(value))
    elif isinstance(data, str):
        topics.append(data)
    return topics

# Load topics from JSON (supports nested structure)
try:
    with open(TOPIC_JSON_FILE, "r", encoding="utf-8") as f:
        _raw = json.load(f)
    search_topics = sorted(set(_extract_topics(_raw)))
    if not search_topics:
        print("⚠️ No search topics found in search_topics.json. Nothing to search.")
except FileNotFoundError:
    print(f"❌ Topics file not found: {TOPIC_JSON_FILE}. Nothing to search.")
    search_topics = []
except json.JSONDecodeError as e:
    print(f"❌ Failed to parse {TOPIC_JSON_FILE}: {e}. Nothing to search.")
    search_topics = []

# Function to search Google Dataset Search
def search_google_datasets(query):
    # Use quoted term to reduce noise
    formatted_query = ('"' + query.replace('"', ' ') + '"').replace(" ", "+")
    base_url = GOOGLE_SEARCH_URL.format(formatted_query)

    print(f"\n🔍 Searching: {query}")

    def fetch(url):
        try:
            resp = requests.get(url, headers=HEADERS, timeout=20)
            return resp
        except requests.RequestException as e:
            print(f"❌ Request error for {query}: {e}")
            return None

    def is_blocked(resp_text, resp_url):
        tl = resp_text.lower()
        return (
            "unusual traffic" in tl or
            "recaptcha" in tl or
            "verify you're not a robot" in tl or
            "form action=\"https://consent.google.com/save\"" in tl or
            (resp_url and "consent.google.com" in resp_url)
        )

    def parse_results(soup_obj):
        items = []
        # Prefer standard containers
        containers = soup_obj.select("div.tF2Cxc, div.g, div#search div.g")
        for c in containers:
            a_tag = c.select_one("a[href]")
            title_el = c.select_one("h3")
            if not a_tag or not title_el:
                continue
            href = a_tag.get("href", "")
            # Normalize Google redirect links
            if href.startswith("/url?"):
                from urllib.parse import urlparse, parse_qs
                qs = parse_qs(urlparse(href).query)
                real = qs.get("q", [""])[0]
                if real.startswith("http"):
                    href = real
            # Only keep Dataset Search links
            if "datasetsearch.research.google.com" not in href:
                continue
            desc_el = (
                c.select_one("div.IsZvec") or
                c.select_one("div.VwiC3b") or
                c.select_one("span.aCOpRe") or
                c.select_one("div span")
            )
            items.append({
                "title": title_el.get_text(strip=True),
                "link": href,
                "description": desc_el.get_text(strip=True) if desc_el else "No description available",
            })
        # If still empty, scan all anchors as a fallback
        if not items:
            for a in soup_obj.select("a[href]"):
                href = a.get("href", "")
                # Normalize Google redirect links
                if href.startswith("/url?"):
                    from urllib.parse import urlparse, parse_qs
                    qs = parse_qs(urlparse(href).query)
                    real = qs.get("q", [""])[0]
                    if real.startswith("http"):
                        href = real
                if "datasetsearch.research.google.com" not in href:
                    continue
                title_el = a.select_one("h3") or a
                title = title_el.get_text(strip=True)
                if not title:
                    continue
                # Try to find nearby description
                parent = a.find_parent(["div", "li"]) or soup_obj
                desc_el = (
                    parent.select_one("div.IsZvec") or parent.select_one("div.VwiC3b") or parent.select_one("span")
                )
                items.append({
                    "title": title,
                    "link": href,
                    "description": desc_el.get_text(strip=True) if desc_el else "No description available",
                })
        return items

    # First attempt: standard HTML
    resp = fetch(base_url)
    if resp is None:
        return []
    if resp.status_code != 200:
        print(f"❌ Failed to fetch results for {query}. Status Code: {resp.status_code}")
        return []
    if is_blocked(resp.text, getattr(resp, 'url', '')):
        print(f"⛔ Request appears blocked/consent wall for '{query}'. Skipping.")
        return []

    soup = BeautifulSoup(resp.text, "html.parser")
    results = parse_results(soup)

    # Fallback: basic HTML (gbv=1) if nothing parsed
    if not results:
        basic_url = base_url + "&gbv=1"
        resp2 = fetch(basic_url)
        if resp2 and resp2.status_code == 200 and not is_blocked(resp2.text, getattr(resp2, 'url', '')):
            soup2 = BeautifulSoup(resp2.text, "html.parser")
            results = parse_results(soup2)

    if not results:
        print(f"⚠️ No results parsed for '{query}'. Google may have changed markup or blocked the request.")

    return results

# Run searches and store results
all_datasets = {}

for topic in search_topics:
    # Randomized delay between requests to reduce rate limiting
    time.sleep(random.uniform(5, 15))
    all_datasets[topic] = search_google_datasets(topic)

# Save results to JSON
with open("google_datasets.json", "w", encoding="utf-8") as f:
    json.dump(all_datasets, f, indent=4)

print("\n✅ All dataset links saved to google_datasets.json")