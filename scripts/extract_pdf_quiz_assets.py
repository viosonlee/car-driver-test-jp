from __future__ import annotations

from pathlib import Path
from collections import deque

import pypdfium2 as pdfium
from PIL import Image, ImageChops, ImageOps


OUTPUT_DIR = Path("public/signs")
TARGET_SIZE = 384

# Coordinates refer to the 2.5x render used by render_reference_pdf.py.
# Each crop intentionally excludes the Chinese caption so the image does not
# reveal the answer to the learner.
CROPS: dict[str, tuple[int, tuple[int, int, int, int], bool]] = {
    # PDF page 36: regulatory / indication signs.
    "closed_to_large_trucks.png": (36, (182, 762, 282, 855), False),
    "closed_to_motorcycles.png": (36, (182, 1285, 282, 1365), False),
    "closed_to_pedestrians.png": (36, (1500, 1125, 1600, 1215), False),
    "exclusive_bus_lane.png": (36, (1180, 895, 1285, 985), False),
    "parking_permitted.png": (36, (1678, 728, 1768, 830), False),
    "stopping_permitted.png": (36, (1672, 1130, 1775, 1210), False),
    "safe_zone.png": (36, (1820, 1055, 1925, 1145), False),
    "no_u_turn.png": (36, (500, 610, 600, 710), False),
    "no_overtaking_right.png": (36, (500, 720, 600, 820), False),
    "bicycle_crossing.png": (36, (1820, 765, 1925, 855), False),

    # PDF page 37: warning signs. The left-curve variant is the mirrored
    # official counterpart of the right-curve example printed in the table.
    "warning_crossroads.png": (37, (1330, 195, 1450, 305), False),
    "warning_t_junction.png": (37, (1330, 535, 1450, 640), False),
    "warning_y_junction.png": (37, (1330, 700, 1450, 805), False),
    "warning_roundabout_ahead.png": (37, (1330, 870, 1450, 975), False),
    "warning_right_curve.png": (37, (1330, 1050, 1450, 1155), False),
    "warning_left_curve.png": (37, (1330, 1050, 1450, 1155), True),
    "warning_winding_road.png": (37, (1490, 535, 1610, 640), False),
    "warning_railway_crossing.png": (37, (1490, 700, 1610, 805), False),
    "warning_school.png": (37, (1490, 1050, 1610, 1155), False),
    "warning_traffic_light.png": (37, (1490, 1215, 1610, 1320), False),
    "warning_slippery.png": (37, (1650, 195, 1770, 305), False),
    "warning_falling_rocks.png": (37, (1650, 355, 1770, 465), False),
    "warning_uneven_road.png": (37, (1650, 535, 1770, 640), False),
    "warning_merge.png": (37, (1650, 700, 1770, 805), False),
    "warning_lane_ends.png": (37, (1650, 870, 1770, 975), False),
    "warning_road_narrows.png": (37, (1650, 1050, 1770, 1155), False),
    "warning_two_way.png": (37, (1650, 1215, 1770, 1320), False),
    "warning_uphill.png": (37, (1810, 195, 1930, 305), False),
    "warning_downhill.png": (37, (1810, 355, 1930, 465), False),
    "warning_road_work.png": (37, (1810, 535, 1930, 640), False),
    "warning_strong_wind.png": (37, (1810, 700, 1930, 805), False),
    "warning_animals.png": (37, (1810, 870, 1930, 975), False),
    "warning_other_dangers.png": (37, (1810, 1050, 1930, 1155), False),

    # PDF pages 38-39: representative road markings and road-surface signs.
    "marking_no_u_turn.png": (38, (225, 215, 340, 365), False),
    "marking_speed_limit_30.png": (38, (490, 985, 610, 1090), False),
    "marking_no_entry_zone.png": (38, (490, 1135, 610, 1360), False),
    "marking_bus_lane.png": (38, (1440, 730, 1620, 875), False),
    "marking_pedestrian_crossing.png": (39, (445, 205, 625, 345), False),
    "marking_bicycle_crossing.png": (39, (445, 1235, 625, 1370), False),
    "marking_safety_zone.png": (39, (1470, 540, 1635, 740), False),
    "marking_guide_zone.png": (39, (1740, 245, 1945, 520), False),
}


def find_pdf() -> Path:
    pdfs = sorted(Path.cwd().glob("*.pdf"))
    if not pdfs:
        raise SystemExit("No reference PDF found in the repository root")
    return pdfs[0]


def largest_component_bounds(mask: Image.Image) -> tuple[int, int, int, int] | None:
    pixels = mask.load()
    width, height = mask.size
    visited = bytearray(width * height)
    largest: tuple[int, tuple[int, int, int, int]] | None = None

    for y in range(height):
        for x in range(width):
            offset = y * width + x
            if visited[offset] or not pixels[x, y]:
                continue
            visited[offset] = 1
            queue = deque([(x, y)])
            count = 0
            left = right = x
            top = bottom = y
            while queue:
                current_x, current_y = queue.popleft()
                count += 1
                left = min(left, current_x)
                right = max(right, current_x)
                top = min(top, current_y)
                bottom = max(bottom, current_y)
                for next_x, next_y in (
                    (current_x - 1, current_y),
                    (current_x + 1, current_y),
                    (current_x, current_y - 1),
                    (current_x, current_y + 1),
                ):
                    if not (0 <= next_x < width and 0 <= next_y < height):
                        continue
                    next_offset = next_y * width + next_x
                    if visited[next_offset] or not pixels[next_x, next_y]:
                        continue
                    visited[next_offset] = 1
                    queue.append((next_x, next_y))
            bounds = (left, top, right + 1, bottom + 1)
            if largest is None or count > largest[0]:
                largest = (count, bounds)

    return largest[1] if largest else None


def trim_background(image: Image.Image) -> Image.Image:
    background = Image.new("RGB", image.size, image.getpixel((0, 0)))
    difference = ImageChops.difference(image, background).convert("L")
    mask = difference.point(lambda value: 255 if value > 10 else 0)
    bounds = largest_component_bounds(mask)
    if not bounds:
        return image
    left, top, right, bottom = bounds
    margin = 3
    return image.crop((
        max(0, left - margin),
        max(0, top - margin),
        min(image.width, right + margin),
        min(image.height, bottom + margin),
    ))


def square_canvas(image: Image.Image) -> Image.Image:
    image = trim_background(image.convert("RGB"))
    contained = ImageOps.contain(image, (330, 330), Image.Resampling.LANCZOS)
    canvas = Image.new("RGB", (TARGET_SIZE, TARGET_SIZE), "white")
    position = ((TARGET_SIZE - contained.width) // 2, (TARGET_SIZE - contained.height) // 2)
    canvas.paste(contained, position)
    return canvas


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    document = pdfium.PdfDocument(find_pdf())
    rendered_pages: dict[int, Image.Image] = {}

    for filename, (page_number, box, mirror) in CROPS.items():
        if page_number not in rendered_pages:
            rendered_pages[page_number] = document[page_number - 1].render(scale=2.5).to_pil().convert("RGB")
        crop = rendered_pages[page_number].crop(box)
        if mirror:
            crop = ImageOps.mirror(crop)
        square_canvas(crop).quantize(colors=128).save(OUTPUT_DIR / filename, optimize=True)

    print(f"Extracted {len(CROPS)} verified quiz assets from {find_pdf().name}")


if __name__ == "__main__":
    main()
