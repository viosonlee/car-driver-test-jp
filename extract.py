import fitz
import json

pdf_path = '中国語版「交通の教則」 (一般社団法人日本自動車連盟).pdf'
doc = fitz.open(pdf_path)

output = []
for i in range(20): # first 20 pages
    try:
        page = doc.load_page(i)
        text = page.get_text()
        output.append(f"--- PHYSICAL PAGE {i} ---\n{text}")
    except Exception as e:
        output.append(f"--- PHYSICAL PAGE {i} --- ERROR: {e}")

with open('extracted_pages_0_20.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(output))

print("Extraction complete.")
