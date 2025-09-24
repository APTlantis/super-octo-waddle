# Simple tool to pull sections of datasets and save them locally as .parquets

from datasets import load_dataset

# Load the dataset (use the default config and the 'train' split)
dataset = load_dataset("bigcode/the-stack-v2", split="train")

# Define desired programming languages
target_languages = ["go", "html", "python", "rust"]

# Function to filter based on language
def filter_languages(example):
    return example["lang"] in target_languages  # The dataset includes a "lang" column

# Apply filtering
filtered_dataset = dataset.filter(filter_languages)

# Save filtered dataset (Optional: Save to disk as Parquet or JSON)
filtered_dataset.to_parquet("Filtered_Stack_v2.parquet")