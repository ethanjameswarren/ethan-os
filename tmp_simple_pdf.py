from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch()
    page = b.new_page()
    page.goto('file:///C:/Users/ethan/git/ethan-os/tmp_simple_page.html', wait_until='networkidle')
    page.pdf(path='C:/Users/ethan/git/ethan-os/tmp_simple.pdf', width='6in', height='9in', margin={'top':'0','right':'0','bottom':'0','left':'0'}, print_background=True)
    b.close()
import fitz
doc = fitz.open('C:/Users/ethan/git/ethan-os/tmp_simple.pdf')
print('pages', len(doc))
for i in range(len(doc)):
    print(i, doc[i].get_text()[:50])
doc.close()
