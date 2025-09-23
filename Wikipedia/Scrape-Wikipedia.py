import requests
from bs4 import BeautifulSoup
import json
import os
import time
from datetime import datetime

# Load structured search topics JSON
TOPIC_JSON_FILE = "search_topics.json"

with open(TOPIC_JSON_FILE, "r", encoding="utf-8") as f:
    SEARCH_TOPICS = json.load(f)

MAX_BRANCHES = 3  # Follows 3 related links for deeper dataset coverage
ALL_DATASETS = []  # Stores all scraped data for README generation

# Function to generate a structured filename based on category path
def format_filename(category, subcategory, topic, index):
    """Creates a structured filename for datasets."""
    return f"{category}_{subcategory}_{topic}_{index}.json".replace(" ", "_")

def scrape_page(url, depth=0):
    """Scrape a Wikipedia page, extract key data, and follow up to 3 related links."""
    if depth > MAX_BRANCHES:
        return []

    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch {url}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    dataset = []

    # Extract main title & summary
    title = soup.find("h1").text.strip()
    summary = soup.find("p").text.strip() if soup.find("p") else "No summary available"

    dataset.append({
        "title": title,
        "url": url,
        "summary": summary,
        "depth": depth
    })

    # Follow exactly 3 related links, prioritizing relevant disorder topics
    valid_links = []
    for link in soup.find_all("a", href=True):
        href = link["href"]
        full_link = f"https://en.wikipedia.org{href}"

        # Exclude navigation pages, Wikipedia special pages, and duplicates
        if (
            href.startswith("/wiki/") and
            ":" not in href and  # Excludes Wikipedia categories/admin pages
            "Main_Page" not in href and
            "Special:" not in href and
            "index.php" not in href and
            full_link != url  # Prevents looping back
        ):
            valid_links.append(full_link)

        # Prioritize links with relevant medical/psychological keywords
        if any(keyword in href.lower() for keyword in ["disorder", "psychology", "psychiatry", "mental", "treatment", "neurology", "therapy", "illness"]):
            valid_links.insert(0, full_link)  # Push these to the front of the list

    # Recursively scrape the valid links
    for full_link in valid_links[:MAX_BRANCHES]:
        time.sleep(1)  # Prevents overloading Wikipedia's servers
        dataset.extend(scrape_page(full_link, depth + 1))

    return dataset

# Process each structured category & save datasets accordingly
for category, subcategories in SEARCH_TOPICS.items():
    for subcategory, topics in subcategories.items():
        for index, topic in enumerate(topics, start=1):
            print(f"🔍 Scraping topic {index}/{len(topics)} in {category} > {subcategory}: {topic}")

            # Wikipedia search URL format
            search_url = f"https://en.wikipedia.org/w/index.php?search={topic.replace(' ', '+')}"
            dataset = scrape_page(search_url)

            # Format filename
            dataset_filename = format_filename(category, subcategory, topic, index)

            # Save dataset as JSON
            with open(dataset_filename, "w", encoding="utf-8") as f:
                json.dump(dataset, f, indent=4)

            ALL_DATASETS.append({
                "category": category,
                "subcategory": subcategory,
                "topic": topic,
                "file_name": dataset_filename
            })

            print(f"✅ Saved {dataset_filename}")

# Function to calculate total dataset size
def get_total_file_size(directory=".", extension=".json"):
    total_size = 0
    json_count = 0
    for file in os.listdir(directory):
        if file.endswith(extension):
            total_size += os.path.getsize(file)
            json_count += 1
    return total_size / (1024 * 1024), json_count  # Convert bytes to MB

# Get total file size and dataset count
total_size, json_count = get_total_file_size()

# ASCII Art Design (Field of Symbols)
ascii_design = """
╔════════════════════════════════════════╗
║ ░▒▓▓▒░░▒▓▓▒░░▒▓▓▒░░▒▓▓▒░░▒▓▓▒░░▒▓▓▒░║
║ ░▒▓▓▒░░▒▓▓▒░  NARRAVIBE STUDIO  ░▒▓▓▒░║
║ ░▒▓▓▒░░▒▓▓▒░ STRUCTURED DATASETS ░▒▓▓▒░║
║ ░▒▓▓▒░░▒▓▓▒░░▒▓▓▒░░▒▓▓▒░░▒▓▓▒░░▒▓▓▒░║
╚════════════════════════════════════════╝
"""

# Generate detailed README
readme_filename = "DATASET_README.txt"
with open(readme_filename, "w", encoding="utf-8") as f:
    f.write(ascii_design + "\n\n")
    f.write("NarraVibe Studio - Structured Wikipedia Dataset\n")
    f.write("=" * 60 + "\n")
    f.write(f"Total JSON Datasets: {json_count} files\n")
    f.write(f"Total Data Size: {total_size:.2f} MB\n")
    f.write("=" * 60 + "\n\n")
    
    f.write("This dataset includes structured information extracted from Wikipedia,\n")
    f.write("following a branching strategy of 3 levels deep.\n\n")

    f.write("Dataset Categories:\n")
    for dataset in ALL_DATASETS:
        f.write(f"- {dataset['category']} > {dataset['subcategory']} > {dataset['topic']} ({dataset['file_name']})\n")

    # Timestamp
    f.write("\nGenerated By: NarraVibe Studio - " + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n")

print(f"🚀 Scrape completed! README generated: {readme_filename}")