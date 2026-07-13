from pathlib import Path
from PIL import Image, ImageDraw


PUBLIC_DIR = Path("public")


def create_icon(size: int, output: str, maskable: bool = False) -> None:
    image = Image.new("RGB", (size, size), "#182848")
    draw = ImageDraw.Draw(image)
    margin = int(size * (0.12 if maskable else 0.07))
    draw.rounded_rectangle(
        (margin, margin, size - margin, size - margin),
        radius=int(size * 0.18),
        fill="#4b6cb7",
    )

    # Japanese-style prohibition sign surrounding a simple car silhouette.
    center = size // 2
    radius = int(size * 0.31)
    stroke = max(8, int(size * 0.065))
    draw.ellipse(
        (center - radius, center - radius, center + radius, center + radius),
        fill="#ffffff",
        outline="#ef4444",
        width=stroke,
    )
    car_left, car_right = int(size * 0.30), int(size * 0.70)
    car_top, car_bottom = int(size * 0.43), int(size * 0.62)
    draw.rounded_rectangle(
        (car_left, car_top, car_right, car_bottom),
        radius=int(size * 0.035),
        fill="#182848",
    )
    draw.polygon(
        [
            (int(size * 0.38), car_top),
            (int(size * 0.44), int(size * 0.35)),
            (int(size * 0.60), int(size * 0.35)),
            (int(size * 0.66), car_top),
        ],
        fill="#182848",
    )
    wheel_radius = int(size * 0.045)
    for wheel_x in (int(size * 0.38), int(size * 0.62)):
        draw.ellipse(
            (wheel_x - wheel_radius, car_bottom - wheel_radius, wheel_x + wheel_radius, car_bottom + wheel_radius),
            fill="#111827",
        )
    draw.line(
        (int(size * 0.30), int(size * 0.70), int(size * 0.70), int(size * 0.30)),
        fill="#ef4444",
        width=stroke,
    )
    image.save(PUBLIC_DIR / output, "PNG", optimize=True)


def main() -> None:
    PUBLIC_DIR.mkdir(exist_ok=True)
    create_icon(192, "pwa-192x192.png")
    create_icon(512, "pwa-512x512.png")
    create_icon(512, "pwa-maskable-512x512.png", maskable=True)
    create_icon(180, "apple-touch-icon.png")
    create_icon(48, "favicon-48x48.png")
    print("Generated PWA icons")


if __name__ == "__main__":
    main()
