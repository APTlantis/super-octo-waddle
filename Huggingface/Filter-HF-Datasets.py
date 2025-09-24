import argparse
import os
from datasets import load_dataset, concatenate_datasets

# Default frontend & API-related languages to include
DEFAULT_LANGUAGES = [
    "Python", "Go", "PHP", "Shell", "Nginx", "Dockerfile",
    "HTML", "CSS", "Sass", "Less", "Stylus", "JavaScript", "TypeScript", "Vue", "JSX",
    "Jinja", "Markdown", "JSON", "YAML", "TOML", "Makefile"
]

# Default repos (can be overridden via CLI)
DEFAULT_REPOS = [
    "bigcode/the-stack",
    "bigcode/the-stack_v2",
    "bigcode/starcoderdata",
    "bigcode/starcoder2data-extras",
]


def parse_args():
    parser = argparse.ArgumentParser(description="Filter multiple Hugging Face datasets by language and save as .parquet and .jsonl")
    parser.add_argument(
        "--repos",
        nargs="+",
        default=DEFAULT_REPOS,
        help="List of Hugging Face dataset repos to load (e.g., bigcode/the-stack bigcode/the-stack_v2)",
    )
    parser.add_argument(
        "--languages",
        nargs="+",
        default=DEFAULT_LANGUAGES,
        help="Languages to keep (matches the 'language' field in the datasets)",
    )
    parser.add_argument(
        "--split",
        default="train",
        help="Split to load from each dataset (default: train)",
    )
    parser.add_argument(
        "--cache_dir",
        default="S:/HF-Datasets/the-stack",
        help="Cache directory for datasets (can be on external drive)",
    )
    parser.add_argument(
        "--output_dir",
        default="S:/HF-Datasets/the-stack/Coding-Dataset",
        help="Directory to write output files",
    )
    parser.add_argument(
        "--output_name",
        default="filtered_combined",
        help="Base filename (without extension) for outputs",
    )
    parser.add_argument(
        "--no_parquet",
        action="store_true",
        help="Skip writing .parquet output",
    )
    parser.add_argument(
        "--no_jsonl",
        action="store_true",
        help="Skip writing .jsonl output",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    print("🔹 Configuration:")
    print(f"   - Repos: {args.repos}")
    print(f"   - Split: {args.split}")
    print(f"   - Languages: {args.languages}")
    print(f"   - Cache dir: {args.cache_dir}")
    print(f"   - Output dir: {args.output_dir}")

    datasets_list = []

    def language_filter(example):
        # Use .get to be robust if 'language' is missing; treat missing as not selected
        return example.get("language") in set(args.languages)

    for repo in args.repos:
        try:
            print(f"🔹 Loading dataset: {repo} (split={args.split}) ...")
            ds = load_dataset(repo, cache_dir=args.cache_dir, split=args.split)
        except Exception as e:
            print(f"⚠️ Failed to load {repo}: {e}")
            continue

        print(f"   - Filtering by languages ({len(args.languages)} values)...")
        try:
            filtered_ds = ds.filter(language_filter)
        except Exception as e:
            print(f"⚠️ Filtering failed for {repo} (possibly missing 'language' field): {e}")
            print("   - Proceeding without filtering for this repo.")
            filtered_ds = ds

        count = len(filtered_ds)
        print(f"   - Kept {count} rows after filtering")
        if count > 0:
            datasets_list.append(filtered_ds)
        else:
            print("   - Skipping empty filtered result for this repo.")

    if not datasets_list:
        print("❌ No datasets were loaded or remained after filtering. Nothing to save.")
        return

    if len(datasets_list) == 1:
        combined = datasets_list[0]
    else:
        print(f"🔹 Concatenating {len(datasets_list)} filtered datasets...")
        combined = concatenate_datasets(datasets_list)

    print(f"✅ Combined dataset size: {len(combined)} rows")

    # Save outputs
    parquet_path = os.path.join(args.output_dir, f"{args.output_name}.parquet")
    jsonl_path = os.path.join(args.output_dir, f"{args.output_name}.jsonl")

    if not args.no_parquet:
        print(f"💾 Writing Parquet → {parquet_path}")
        combined.to_parquet(parquet_path)
    else:
        print("⏭️ Skipping Parquet output as requested")

    if not args.no_jsonl:
        print(f"💾 Writing JSONL → {jsonl_path}")
        combined.to_json(jsonl_path)
    else:
        print("⏭️ Skipping JSONL output as requested")

    print("🎉 Done.")


if __name__ == "__main__":
    main()