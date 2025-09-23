import json
from urllib.parse import urlencode
from urllib.request import urlopen

# Topics to search for on Project Gutenberg (via Gutendex API)
topics = ["cliffsnotes", "summary"]

# Collect unique Gutenberg book IDs across topics
book_ids = set()

for topic in topics:
    print(f"🔍 Searching for books on: {topic}")
    # Query Gutendex API for the topic
    params = urlencode({"search": topic})
    url = f"https://gutendex.com/books?{params}"
    try:
        with urlopen(url) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            results = data.get("results", [])
            for item in results:
                # Each item should have an 'id' (Gutenberg book id) and 'title'
                bid = item.get("id")
                title = (item.get("title") or "").lower()
                if bid is not None:
                    # Extra guard: ensure the topic is in the title (case-insensitive)
                    if topic.lower() in title or topic.lower() in (item.get("subjects") or []):
                        book_ids.add(int(bid))
    except Exception as e:
        print(f"⚠️ Failed to query Gutendex for '{topic}': {e}")

print(f"\n📚 Found {len(book_ids)} books matching our topics!")

with open("Gutenberg-Book-Ids.txt", "w", encoding="utf-8") as f:
    for book_id in sorted(book_ids):
        f.write(str(book_id) + "\n")

print("✅ Book IDs saved to `Gutenberg-Book-Ids.txt`.")
