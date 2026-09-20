from playwright.sync_api import sync_playwright
html = r'file:///C:/Users/ethan/git/ethan-life/reports/hobby/warhammer-40k-necron-dynasty/lore-book/2026/lore-book.html'
pdf = r'C:/Users/ethan/git/ethan-life/reports/hobby/warhammer-40k-necron-dynasty/lore-book/2026/lore-book-nosize.pdf'
with sync_playwright() as p:
    b = p.chromium.launch()
    page = b.new_page()
    page.goto(html, wait_until='networkidle', timeout=120000)
    page.pdf(path=pdf, margin={'top':'0','right':'0','bottom':'0','left':'0'}, print_background=True)
    b.close()
import fitz
doc = fitz.open(pdf)
print('pages', len(doc))
for i in range(min(5, len(doc))):
    print(i, doc[i].get_text()[:80].replace('\n',' '))
for i in range(len(doc)):
    r = doc[i].rect
    print(i, r.width, r.height)
doc.close()
