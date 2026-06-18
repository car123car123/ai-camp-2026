#!/usr/bin/env python3
# ---------------------------------------------------------------
# make_cars.py  –  Generates two simple PNG cars for la_car_sim.py
#
# Run once:   python3 ~/Desktop/make_cars.py
# Output:     supra.png   (red rectangle)
#             skyra.png   (blue rectangle)
# ---------------------------------------------------------------

import os, sys
from PIL import Image, ImageDraw

def make_rect(name, width, height, color):
    """Create a single coloured rectangle PNG."""
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))   # transparent background
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, width-1, height-1], fill=color)  # border‑less rectangle
    img.save(f'{name}.png')
    print(f'✅ {name}.png created ({width}×{height})')

if __name__ == "__main__":
    # Ensure the script runs from the Desktop folder
    os.chdir(os.path.expanduser("~/Desktop"))

    # 1️⃣ Supra – red rectangle, size ~60x30 px
    make_rect('supra', 60, 30, (255, 0, 0, 255))

    # 2️⃣ Skyline – blue rectangle, same size
    make_rect('skyra', 60, 30, (0, 0, 255, 255))
