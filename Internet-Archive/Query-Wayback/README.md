# Query-Wayback

Enumerate Wayback Machine snapshots for a given domain and save a compact JSON report.

## What this script does

- Uses waybackpy's CDX Server API client to iterate snapshots for the configured domain
- Writes a list of objects with `archive_url` and `length` fields to `snapshots.json`

## Requirements

- Python 3.8+
- waybackpy

Install:
```powershell
python -m pip install --upgrade pip
pip install waybackpy
```

Optional virtual environment:
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install waybackpy
```

## Usage

1) Change directory to this folder:
```powershell
cd D:\All-Pojects\SCRAPERS\Internet-Archive\Query-Wayback
```

2) (Optional) Edit the target domain and User-Agent in the script:
- Open `Query-Wayback.py`
- Modify this line to your target domain and a descriptive User-Agent:
  `WaybackMachineCDXServerAPI("linuxtracker.org", user_agent="aptlantisbot/1.0")`

3) Run the script:
```powershell
python .\Query-Wayback.py
```

4) Inspect the output file:
- `snapshots.json` is created in this folder

Example output (abbreviated and valid JSON):
```json
[
  {"archive_url": "http://web.archive.org/web/20190101010101/http://example.com/", "length": 12345},
  {"archive_url": "http://web.archive.org/web/20200102030405/http://example.com/about", "length": 67890}
]
```

## Notes and tips

- If you see throttling or HTTP errors, slow down and ensure you use a reasonable User-Agent.
- Some domains have many snapshots; the script will iterate through all available ones. Consider adding filters if needed.
- Output schema is minimal by design; expand it in the loop if you need more fields from `page`.
