from pypdf import PdfReader
r = PdfReader(r'C:\Users\ethan\git\ethan-life\reports\hobby\warhammer-40k-necron-dynasty\lore-book\2026\lore-book.pdf')
print('pypdf pages', len(r.pages))
for i, p in enumerate(r.pages[:10]):
    w = float(p.mediabox.width)
    h = float(p.mediabox.height)
    print(i, w, h, w/72, h/72)
