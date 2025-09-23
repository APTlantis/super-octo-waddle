import requests
import json

# Internet Archive API Base URL
IA_API_URL = "https://archive.org/advancedsearch.php"

# Topics to search for
search_topics = [
    "Quantum Computing", "Artificial Intelligence", "Logic",
    "Cryptography", "Encryption", "Problem Solving",
    "Mathematical Logic", "Automated Theorem Proving",
    "Post-Quantum Cryptography", "Blockchain Security",
    "Zero-Knowledge Proofs", "Homomorphic Encryption"
]

# Function to search Internet Archive
def search_internet_archive(topic):
    print(f"\n🔍 Searching Internet Archive for: {topic}")
    
    params = {
        "q": topic,
        "fl[]": "identifier,title,year,mediatype,format",
        "output": "json",
        "rows": 20  # Adjust this for more results
    }

    response = requests.get(IA_API_URL, params=params)
    
    if response.status_code == 200:
        results = response.json()["response"]["docs"]
        datasets = []

        for item in results:
            datasets.append({
                "title": item.get("title", "Unknown Title"),
                "year": item.get("year", "Unknown Year"),
                "id": item["identifier"],
                "media_type": item.get("mediatype", "Unknown"),
                "formats": item.get("format", [])
            })
        
        return datasets
    else:
        print(f"❌ Error fetching results for {topic}. Status Code: {response.status_code}")
        return []

# Run search for all topics
all_datasets = {}

for topic in search_topics:
    all_datasets[topic] = search_internet_archive(topic)

# Save results to JSON
with open("internet_archive.json", "w", encoding="utf-8") as f:
    json.dump(all_datasets, f, indent=4)

print("\n✅ All dataset links saved to internet_archive.json")