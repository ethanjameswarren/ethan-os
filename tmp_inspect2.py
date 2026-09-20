import fitz
path = r'C:\Users\ethan\git\ethan-life\reports\hobby\warhammer-40k-necron-dynasty\lore-book\2026\lore-book.pdf'
doc = fitz.open(path)
for i in range(min(20, len(doc))):
    page = doc[i]
    txt = page.get_text().strip().replace('\n',' ')[:200]
    print(f'{i}: {txt!r}')
doc.close()
