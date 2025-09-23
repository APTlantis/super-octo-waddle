import gutenbergpy.textget

# ✅ Load Book IDs from the File
with open("Gutenberg-Book-Ids.txt", "r") as f:
    book_ids = [line.strip() for line in f.readlines()]

print(f"📥 Downloading {len(book_ids)} books from Project Gutenberg...")

for book_id in book_ids:
    try:
        print(f"📖 Downloading Book ID: {book_id}")
        book_text = gutenbergpy.textget.get_text_by_id(int(book_id))
        
        # ✅ Save Each Book as a Text File
        with open(f"Gutenberg-Books/Book_{book_id}.txt", "w", encoding="utf-8") as f:
            f.write(book_text.decode("utf-8"))

    except Exception as e:
        print(f"❌ Failed to download Book ID {book_id}: {e}")

print("\n🎉 All books downloaded successfully! Check the `Gutenberg-Books/` folder.")