from pathlib import Path
import json
import sys

from rapidocr_onnxruntime import RapidOCR


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit("usage: ocr_reference_pdf.py IMAGE_DIR OUTPUT_JSON")

    image_dir = Path(sys.argv[1])
    output_path = Path(sys.argv[2])
    engine = RapidOCR()
    pages = []

    for image_path in sorted(image_dir.glob("page-*.png")):
        result, _ = engine(str(image_path))
        lines = []
        for item in result or []:
            box, text, confidence = item
            lines.append({"text": text, "confidence": confidence, "box": box})
        pages.append({
            "page": int(image_path.stem.split("-")[-1]),
            "text": "\n".join(line["text"] for line in lines),
            "lines": lines,
        })
        print(f"OCR {image_path.name}: {len(lines)} lines", flush=True)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(pages, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {output_path}")


if __name__ == "__main__":
    main()
