import requests
from bs4 import BeautifulSoup
import json

LEGAL_URL = "https://www.courtlistener.com/opinion/"

def scrape_legal_cases():
    case_data = []
    for i in range(1, 5):  # Scraping first 5 pages
        response = requests.get(f"{LEGAL_URL}?page={i}")
        if response.status_code != 200:
            print("Failed to fetch legal cases")
            return []

        soup = BeautifulSoup(response.text, "html.parser")
        for case in soup.find_all("div", class_="opinions"):
            case_title = case.find("h4").text.strip()
            case_link = case.find("a")["href"]
            case_data.append({"title": case_title, "url": f"https://www.courtlistener.com{case_link}"})

    return case_data

def save_json(data, filename="legal_cases.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

legal_cases = scrape_legal_cases()
save_json(legal_cases)

print(f"✅ Scraped {len(legal_cases)} legal cases!")