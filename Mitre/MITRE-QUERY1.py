import requests
from bs4 import BeautifulSoup
import json
import time

# Base URL for MITRE ATT&CK techniques
BASE_URL = "https://attack.mitre.org/techniques/enterprise/"

# Function to scrape MITRE ATT&CK techniques
def scrape_mitre_attack():
    print("🔍 Scraping MITRE ATT&CK database...")
    response = requests.get(BASE_URL)
    if response.status_code != 200:
        print(f"❌ Failed to access {BASE_URL}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    techniques = []

    # Find all techniques on the page
    table_rows = soup.find_all("tr")
    for row in table_rows:
        cells = row.find_all("td")
        if len(cells) < 2:
            continue  # Skip rows that don't contain enough data

        # Ensure the second cell has a link
        link_element = cells[1].find("a")
        if not link_element or "href" not in link_element.attrs:
            print(f"⚠️ Skipping row with missing link: {cells[1].text.strip()}")
            continue  # Skip rows without links

        technique_id = cells[0].text.strip()
        technique_name = cells[1].text.strip()
        technique_link = f"https://attack.mitre.org{link_element['href']}"

        # Extract details from individual technique pages
        technique_data = scrape_technique_details(technique_link)
        techniques.append({
            "technique_id": technique_id,
            "technique_name": technique_name,
            "url": technique_link,
            **technique_data
        })

        print(f"✅ Scraped: {technique_name} ({technique_id})")
        time.sleep(2)  # Pause to avoid overwhelming the server

    return techniques

# Function to scrape details from individual technique pages
def scrape_technique_details(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"❌ Failed to fetch details for {url}")
        return {}

    soup = BeautifulSoup(response.text, "html.parser")
    details = {}

    # Extract description
    desc_section = soup.find("div", class_="description-body")
    details["description"] = desc_section.text.strip() if desc_section else "No description available."

    # Extract threat groups associated with this technique
    threat_groups = []
    threat_table = soup.find("table", class_="table-mitre matrix")
    if threat_table:
        for row in threat_table.find_all("tr")[1:]:
            cells = row.find_all("td")
            if len(cells) >= 2:
                group_name = cells[0].text.strip()
                threat_groups.append(group_name)
    details["associated_threat_groups"] = threat_groups

    return details

# Run scraper and save results
mitre_attack_data = scrape_mitre_attack()
output_filename = "MITRE_ATTACK_Dataset.json"

with open(output_filename, "w", encoding="utf-8") as f:
    json.dump(mitre_attack_data, f, indent=4)

print(f"🚀 MITRE ATT&CK data saved as {output_filename}")