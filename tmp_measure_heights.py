from playwright.sync_api import sync_playwright
html = r'file:///C:/Users/ethan/git/ethan-life/reports/hobby/warhammer-40k-necron-dynasty/lore-book/2026/lore-book.html'
with sync_playwright() as p:
    b = p.chromium.launch()
    page = b.new_page()
    page.goto(html, wait_until='networkidle', timeout=120000)
    data = page.evaluate("""() => {
        const pages = Array.from(document.querySelectorAll('.book-page'));
        return {
            bodyHeight: document.body.scrollHeight,
            pageHeights: pages.map(p => ({ id: p.id, clientH: p.clientHeight, scrollH: p.scrollHeight }))
        };
    }""")
    b.close()
print('body height', data['bodyHeight'])
for p in data['pageHeights'][:10]:
    print(p)
