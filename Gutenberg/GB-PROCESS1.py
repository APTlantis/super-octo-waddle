import json
from transformers import AutoTokenizer
import os

# ✅ Load TinyLlama Tokenizer
tokenizer = AutoTokenizer.from_pretrained("TinyLlama/TinyLlama-1.1B-intermediate-step-1431k-3T")

# ✅ Convert Books to JSONL Format
output_file = "Gutenberg-Books-Tokenized.jsonl"
with open(output_file, "w", encoding="utf-8") as f_out:
    for book_file in os.listdir("Gutenberg-Books"):
        if book_file.endswith(".txt"):
            with open(f"Gutenberg-Books/{book_file}", "r", encoding="utf-8") as f_in:
                text = f_in.read()
                tokens = tokenizer.encode(text, truncation=True, max_length=2048)

                json.dump({"input_ids": tokens, "labels": tokens}, f_out)
                f_out.write("\n")

print(f"\n🎉 Tokenized books saved to `{output_file}`!")