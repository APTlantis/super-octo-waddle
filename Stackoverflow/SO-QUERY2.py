import requests
import json
import time

# 🔥 Your Stack Overflow API Key
API_KEY = "rl_q36MRhHAFhhFph5NVNgCfrQDU"

# 🏆 Priority-based topic search
TOPICS = [
    # 🥇 Priority 1 - Heavy Focus
    "Golang", "Go language", "Go concurrency", "Go microservices",
    
    # 🥇 Priority 1 - Heavy Focus
    "Python", "Python scripting", "Python automation", "Python Flask", "Python Django", "Python FastAPI",
    
    # 🥈 Priority 2 - Databases
    "SQL", "PostgreSQL", "MySQL", "SQLite", "Redis", "MongoDB", "NoSQL",
    
    # 🥉 Priority 3 - Backend / API Development
    "REST API", "GraphQL", "FastAPI", "Flask API", "Django API", "Microservices", "Backend development",

    # 🏅 Priority 4 - OpenAI / LLM Development
    "OpenAI API", "ChatGPT API", "GPT fine-tuning", "LLM training", "Prompt engineering",
]

# ⏳ Stack Overflow API URL
BASE_URL = "https://api.stackexchange.com/2.3/search"

# 🔥 Data storage
all_questions = []

for topic in TOPICS:
    print(f"🔍 Searching Stack Overflow for: {topic}")

    params = {
        "order": "desc",
        "sort": "relevance",
        "intitle": topic,
        "site": "stackoverflow",
        "pagesize": 50,  # Fetch 50 questions per topic
        "key": API_KEY
    }

    response = requests.get(BASE_URL, params=params)
    data = response.json()

    if "items" in data:
        all_questions.extend(data["items"])
        print(f"✅ Found {len(data['items'])} questions for: {topic}")

    # ⏳ Avoid hitting rate limits
    time.sleep(2)

# 💾 Save results to JSON
with open("stack_overflow_questions.json", "w") as f:
    json.dump(all_questions, f, indent=4)

print("🔥 DONE! Stack Overflow data saved for fine-tuning.")