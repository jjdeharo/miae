#!/usr/bin/env python3
"""Build MIAE's font-independent SVG, ICO and Apple touch icon."""
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
POINTS = [(14, 48), (14, 16), (22, 16), (32, 35), (42, 16), (50, 16),
          (50, 48), (42, 48), (42, 30), (35, 43), (29, 43), (22, 30), (22, 48)]
BACKGROUND = '#172033'
points = ' '.join(f'{x},{y}' for x, y in POINTS)
(ROOT / 'assets/favicon.svg').write_text(
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">\n'
    '  <title>MIAE</title>\n'
    f'  <rect width="64" height="64" rx="10" fill="{BACKGROUND}"/>\n'
    f'  <polygon points="{points}" fill="#fff"/>\n'
    '</svg>\n'
)

def render(size, rounded=True):
    scale = 8
    image = Image.new('RGBA', (size * scale, size * scale), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    factor = size * scale / 64
    draw.rounded_rectangle((0, 0, size * scale - 1, size * scale - 1),
                           radius=10 * factor if rounded else 0, fill=BACKGROUND)
    draw.polygon([(round(x * factor), round(y * factor)) for x, y in POINTS], fill='white')
    return image.resize((size, size), Image.Resampling.LANCZOS)

render(64).save(ROOT / 'favicon.ico', sizes=[(16, 16), (32, 32), (48, 48), (64, 64)])
render(180, rounded=False).convert('RGB').save(ROOT / 'assets/apple-touch-icon.png')
print('Generated SVG favicon, four-size ICO and Apple touch icon.')
