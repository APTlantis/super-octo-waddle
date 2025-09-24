import arxiv
import requests

# ✅ Search for AI & Ethics Research Papers
search = arxiv.Search(
    query="Artificial Intelligence Ethics",
    max_results=10,
    sort_by=arxiv.SortCriterion.SubmittedDate
)

# ✅ Download PDF of each paper
for paper in search.results():
    pdf_url = paper.pdf_url
    print(f"Downloading: {paper.title}")
    response = requests.get(pdf_url)
    with open(f"{paper.title}.pdf", "wb") as f:
        f.write(response.content)

print("📜 Downloaded AI & Ethics papers from ArXiv!")