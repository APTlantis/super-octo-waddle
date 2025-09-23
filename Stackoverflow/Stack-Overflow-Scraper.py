import requests
import jsonlines
import time

# Stack Overflow API Base URL
BASE_URL = "https://api.stackexchange.com/2.3/questions"

# Topics/tags to scrape
tags = ["python", "machine-learning", "deep-learning", "ai", "neural-networks",
        "data-science", "sql", "database", "encryption", "security"]

# Query Parameters
params = {
    "order": "desc",
    "sort": "votes",
    "site": "stackoverflow",
    "pagesize": 100,  # Max per request
    "tagged": ";".join(tags),
    "filter": "!9_bDDxJY5"  # Returns answers and body content
}

# Output file
output_file = "Stack-Overflow-Query.jsonl"

# Scrape Stack Overflow
with jsonlines.open(output_file, mode="w") as writer:
    page = 1
    while page <= 5:  # Adjust based on data needs
        params["page"] = page
        response = requests.get(BASE_URL, params=params)

        if response.status_code == 200:
            data = response.json()["items"]
            for question in data:
                # Extract relevant fields
                scraped_data = {
                    "title": question["title"],
                    "question_body": question.get("body", ""),
                    "answers": [ans["body"] for ans in question.get("answers", []) if ans["is_accepted"]],
                    "tags": question["tags"],
                    "link": question["link"]
                }
                writer.write(scraped_data)
                print(f"✅ Scraped: {question['title']}")

        else:
            print(f"❌ Error fetching page {page}: {response.status_code}")

        time.sleep(1)  # Avoid rate limits
        page += 1

print(f"🔥 Stack Overflow dataset saved! ✅")