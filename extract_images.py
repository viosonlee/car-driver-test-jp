import fitz

pdf_path = '中国語版「交通の教則」 (一般社団法人日本自動車連盟).pdf'
doc = fitz.open(pdf_path)

for i in range(3, 15):
    page = doc.load_page(i)
    images = page.get_images(full=True)
    for j, img in enumerate(images):
        xref = img[0]
        base_image = doc.extract_image(xref)
        image_bytes = base_image["image"]
        image_ext = base_image["ext"]
        with open(f"page_{i}_img_{j}.{image_ext}", "wb") as f:
            f.write(image_bytes)
