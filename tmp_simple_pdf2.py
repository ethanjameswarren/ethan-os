from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch()
    page = b.new_page()
    page.goto('file:///C:/Users/ethan/git/ethan-os/tmp_simple_page2.html', wait_until='networkidle')
    page.pdf(path='C:/Users/ethan/git/ethan-os/tmp_simple2.pdf', width='6in', height='9in', margin={'top':'0','right':'0','bottom':'0','left':'0'}, print_background=True)
    b.close()
import fitz
doc = fitz.open('C:/Users/ethan/git/ethan-os/tmp_simple2.pdf')
print('pages', len(doc))
for i in range(len(doc)):
    txt = doc[i].get_text().strip().replace('\n',' ')[:200]
    print(i, txt)
doc.close()
