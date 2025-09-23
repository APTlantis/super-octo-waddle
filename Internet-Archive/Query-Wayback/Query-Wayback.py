import json
from waybackpy import WaybackMachineCDXServerAPI

cdx = WaybackMachineCDXServerAPI("linuxtracker.org", user_agent="aptlantisbot/1.0")
results = []

for page in cdx.snapshots():
    results.append({
        "archive_url": page.archive_url,
        "length": page.length
    })

with open("snapshots.json", "w") as f:
    json.dump(results, f, indent=2)