import fitz
path = r'C:\Users\ethan\git\ethan-life\reports\hobby\warhammer-40k-necron-dynasty\lore-book\2026\lore-book.pdf'
doc = fitz.open(path)
print('pages', len(doc))
for i in range(min(10, len(doc))):
    page = doc[i]
    print(i, page.rect, page.get_text()[:100].replace('\n',' '))
doc.close()
