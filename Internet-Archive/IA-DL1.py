import json
import os
import requests

# Load dataset links from JSON
with open("internet_archive.json", "r", encoding="utf-8") as f:
    dataset_info = json.load(f)

# Create a folder for downloads
DATASET_DIR = "internet_archive_datasets"
os.makedirs(DATASET_DIR, exist_ok=True)

# Function to download datasets
def download_file(identifier, filename):
    url = f"https://archive.org/download/{identifier}/{filename}"
    
    try:
        print(f"⬇️ Downloading: {url}")
        response = requests.get(url, stream=True, timeout=10)
        response.raise_for_status()

        filepath = os.path.join(DATASET_DIR, filename)
        with open(filepath, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        print(f"✅ Saved: {filepath}\n")

    except Exception as e:
        print(f"❌ Failed to download {url}: {e}")

# Loop through datasets and download files
for topic, datasets in dataset_info.items():
    print(f"\n🔍 Downloading datasets for: {topic}")

    for dataset in datasets:
        identifier = dataset["id"]
        formats = dataset["formats"]

        # Pick a preferred format
        for preferred_format in ["PDF", "CSV", "JSON", "TXT"]:
            for fmt in formats:
                if preferred_format in fmt:
                    filename = f"{identifier}.{preferred_format.lower()}"
                    download_file(identifier, filename)

print("\n✅ All possible datasets downloaded!")