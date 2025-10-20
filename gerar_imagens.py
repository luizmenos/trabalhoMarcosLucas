import os
import random
from PIL import Image, ImageDraw

output_dir = "data/input"
os.makedirs(output_dir, exist_ok=True)

for i in range(30):

    w, h = random.randint(200, 800), random.randint(200, 800)


    color = tuple(random.randint(0, 255) for _ in range(3))
    img = Image.new("RGB", (w, h), color)


    draw = ImageDraw.Draw(img)
    for _ in range(10):
        x1, y1 = random.randint(0, w), random.randint(0, h)
        x2, y2 = random.randint(0, w), random.randint(0, h)
        
        x1, x2 = sorted([x1, x2])
        y1, y2 = sorted([y1, y2])
        shape_color = tuple(random.randint(0, 255) for _ in range(3))
        draw.rectangle([x1, y1, x2, y2], outline=shape_color, width=3)


    filename = os.path.join(output_dir, f"img_{i+1:02d}.jpg")
    img.save(filename, "JPEG")
