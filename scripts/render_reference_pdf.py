from pathlib import Path
import sys

import pypdfium2 as pdfium


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit("usage: render_reference_pdf.py PDF OUTPUT_DIR")

    pdf_path = Path(sys.argv[1])
    output_dir = Path(sys.argv[2])
    output_dir.mkdir(parents=True, exist_ok=True)

    document = pdfium.PdfDocument(pdf_path)
    for index in range(len(document)):
        page = document[index]
        image = page.render(scale=2.5).to_pil()
        image.save(output_dir / f"page-{index + 1:03d}.png", optimize=True)

    print(f"Rendered {len(document)} pages to {output_dir}")


if __name__ == "__main__":
    main()
