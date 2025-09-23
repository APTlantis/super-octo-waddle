# Internet Archive Scrapers

This folder contains small, focused Python scripts that interact with the Internet Archive ecosystem for two common tasks:

- Discovering items on archive.org via the Advanced Search API
- Enumerating Wayback Machine snapshots for a given domain and saving a simple report

The scripts are intentionally minimal and easy to adapt.

## Contents

- IA-QUERY1.py
  - Queries Internet Archive (archive.org) for a predefined list of topics and saves a JSON summary.
- Query-Wayback/Query-Wayback.py
  - Uses waybackpy to iterate Wayback Machine snapshots for a domain and writes them to snapshots.json.

## Requirements

- Python 3.8+ (tested with 3.11)
- pip to install dependencies

Python packages used:
- requests (for IA-QUERY1.py)
- waybackpy (for Query-Wayback/Query-Wayback.py)

Install directly with pip:

```powershell
# From the project root or this folder
python -m pip install --upgrade pip
pip install requests waybackpy
```

Optionally, create and use a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install requests waybackpy
```

## Usage

All examples below assume PowerShell on Windows.

### 1) Search Internet Archive by topics (IA-QUERY1.py)

What it does:
- Searches Internet Archive for multiple topics using the Advanced Search API
- Pulls basic fields: identifier, title, year, mediatype, format
- Saves results to `internet_archive.json` in this folder

Run it:
```powershell
# In D:\All-Pojects\SCRAPERS\Internet-Archive
python .\IA-QUERY1.py
```

Customize topics:
- Open `IA-QUERY1.py`
- Edit the `search_topics` list to include your terms of interest

Output file example (abbreviated):
```json
{
  "Quantum Computing": [
    {
      "title": "Some Item Title",
      "year": "2019",
      "id": "identifier123",
      "media_type": "texts",
      "formats": ["PDF", "Text PDF"]
    }
  ],
  "Artificial Intelligence": []
}
```

Notes:
- Increase or decrease the number of results per topic by changing `rows` in the request params (default is 20).

### 2) List Wayback Machine snapshots for a domain (Query-Wayback/Query-Wayback.py)

What it does:
- Iterates Wayback Machine snapshots for a given domain using `waybackpy`
- Writes a list of `{ archive_url, length }` entries to `snapshots.json` in the `Query-Wayback` folder

Run it:
```powershell
# In D:\All-Pojects\SCRAPERS\Internet-Archive\Query-Wayback
python .\Query-Wayback.py
```

Change the domain:
- Open `Query-Wayback/Query-Wayback.py`
- On line with `WaybackMachineCDXServerAPI("linuxtracker.org", ...)`, change `linuxtracker.org` to the domain you want
- Optionally tweak `user_agent` to something descriptive (e.g., your app/bot name)

Output file example (abbreviated):
```json
[
  {
    "archive_url": "http://web.archive.org/web/20190101010101/http://example.com/",
    "length": 12345
  },
  { "archive_url": "...", "length": 67890 }
]
```

## Troubleshooting

- SSL or connection errors: try again later; the Internet Archive APIs can throttle or experience intermittent issues.
- HTTP 429/403 from Wayback: slow down requests; make sure you use a reasonable User-Agent.
- Empty results: adjust your topics, increase `rows`, or confirm the target domain has snapshots in the Wayback Machine.

## Notes

- These scripts are examples and starting points. Feel free to adapt filtering, fields, or output formats for your needs.
- Be considerate and avoid excessive request rates.
