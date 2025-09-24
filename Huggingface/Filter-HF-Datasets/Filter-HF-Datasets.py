from datasets import load_dataset

# ✅ Set external drive path
external_drive_path = "S:/HF-Datasets/the-stack"

# ✅ Define frontend & API-related languages to download
selected_languages = [
    "Python", "Go", "PHP", "Shell", "Nginx", "Dockerfile",
    "HTML", "CSS", "Sass", "Less", "Stylus", "JavaScript", "TypeScript", "Vue", "JSX",
    "Jinja", "Markdown", "JSON", "YAML", "TOML", "Makefile"
]

# ✅ Load the entire dataset (no `name=` argument needed)
print("🔹 Loading dataset metadata...")
ds = load_dataset("bigcode/the-stack", cache_dir=external_drive_path, split="train")

# ✅ Filter dataset to only keep selected languages
def language_filter(example):
    return example["language"] in selected_languages

print(f"🔹 Filtering dataset for selected languages...")
filtered_ds = ds.filter(language_filter)

# ✅ Save the filtered dataset
filtered_ds.save_to_disk(f"{external_drive_path}/filtered-the-stack")

print(f"✅ Dataset filtered & saved to: {external_drive_path}/filtered-the-stack")