import fitz

pdf_path = '中国語版「交通の教則」 (一般社団法人日本自動車連盟).pdf'
doc = fitz.open(pdf_path)

for i in range(5):
    page = doc.load_page(i)
    images = page.get_images(full=True)
    print(f"Page {i}: {len(images)} images")
