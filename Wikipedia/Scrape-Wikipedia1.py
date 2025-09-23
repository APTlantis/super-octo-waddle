import wikipediaapi
import jsonlines

# Set up Wikipedia API with a proper User-Agent
wiki = wikipediaapi.Wikipedia(
    language="en",
    user_agent="WikiScraperBot/1.0 (https://yourwebsite.com/contact)"
)

# List of Wikipedia articles to scrape
topics = [
    "AI_ethics",
    "Algorithmic_bias",
    "Fairness_of_artificial_intelligence",
    "Bias_in_artificial_intelligence",
    "Encryption",
    "Post-quantum_cryptography",
    "Quantum_cryptography",
    "Homomorphic_encryption",
    "Advanced_Encryption_Standard",
    "End-to-end_encryption",
    "RSA_(cryptosystem)",
    "Elliptic-curve_cryptography",
    "Cryptographic_protocol",
    "Secure_Multi-Party_Computation",
    "Digital_signature",
    "Cybersecurity_standards",
    "Zero-knowledge_proof",
    "Surveillance",
    "Privacy_policy",
    "Data_protection_regulation"
]

# Output file path
output_file = "S:/WIKI-Scrape.jsonl"

# Function to scrape a Wikipedia page and its linked topics
def scrape_wikipedia(title, depth=2, visited=set()):
    if title in visited:
        return  # Avoid re-scraping the same page

    page = wiki.page(title)
    if not page.exists():
        print(f"❌ Page Not Found: {title}")
        return

    visited.add(title)  # Mark this page as visited

    # Save the main article
    with jsonlines.open(output_file, mode="a") as writer:
        article_data = {
            "title": title,
            "content": page.text
        }
        writer.write(article_data)
        print(f"✅ Scraped: {title}")

    # Recursively scrape linked articles (only up to the given depth)
    if depth > 0:
        for link in page.links.keys():
            scrape_wikipedia(link, depth - 1, visited)

# Start the scraping process
try:
    for topic in topics:
        scrape_wikipedia(topic, depth=2)  # Depth 2 means it grabs related articles
    print(f"🔥 Wikipedia dataset saved with expanded topics!")

except Exception as e:
    print(f"🚨 Error during scraping: {e}")