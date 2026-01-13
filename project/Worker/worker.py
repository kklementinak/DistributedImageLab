import redis
import time
import os
import sys
import json
from rembg import remove
try:
    from PIL import Image, ImageFilter, ImageOps, ImageDraw
except ImportError:
    print("Error: Missing libraries. Run: pip install redis pillow")
    sys.exit(1)

try:
    r = redis.Redis(host='localhost', port=6379, db=0)
except:
    print("Error: Redis is not reachable.")
    sys.exit(1)

print(" [*] Mega Worker v4.0 started. Waiting for tasks...")

while True:
    try:
        item = r.brpop('image_queue', timeout=5)
    except:
        continue

    if item:
        try:
            json_str = item[1].decode('utf-8')
            data = json.loads(json_str)
            
            file_path = data['Path']
            rotation = data.get('Rotation', 'none')
            effect = data.get('Effect', 'none')
            watermark_text = data.get('Watermark', '')
            
            print(f" [x] Task: Rotate={rotation}, Effect={effect}, Watermark={watermark_text}")

            if os.path.exists(file_path):
                with Image.open(file_path) as img:
                    
                    if img.mode != 'RGBA' and img.mode != 'RGB':
                        img = img.convert('RGBA')

                    processed = img

                    if rotation == 'left':
                        processed = processed.rotate(90, expand=True)
                    elif rotation == 'right':
                        processed = processed.rotate(-90, expand=True)
                    elif rotation == '180':
                        processed = processed.rotate(180, expand=True)

                    if effect == 'grayscale':
                        processed = processed.convert("L")
                    elif effect == 'sepia':
                        gray = processed.convert("L")
                        processed = ImageOps.colorize(gray, "#704214", "#C0C0C0")
                    elif effect == 'invert':
                        if processed.mode == 'RGBA':
                             processed = processed.convert('RGB')
                        processed = ImageOps.invert(processed)
                    elif effect == 'blur':
                        processed = processed.filter(ImageFilter.GaussianBlur(5))
                    elif effect == 'sharpen':
                        processed = processed.filter(ImageFilter.SHARPEN)
                    elif effect == 'emboss':
                        processed = processed.filter(ImageFilter.EMBOSS)
                    elif effect == 'contour':
                        processed = processed.filter(ImageFilter.CONTOUR)
                    elif effect == 'remove_bg':
                        print(" [.] Running AI Background Removal...")
                        processed = remove(processed)
                    else:
                        processed = img.convert("L")

                    if watermark_text:
                        if processed.mode != 'RGB' and processed.mode != 'RGBA':
                            processed = processed.convert('RGB')
                        
                        draw = ImageDraw.Draw(processed)
                        draw.text((20, 20), watermark_text, fill=(255, 0, 0))
                        print(f" [i] Watermark added.")

                    directory = os.path.dirname(file_path)
                    filename = os.path.basename(file_path)
                    new_path = os.path.join(directory, f"processed_{rotation}_{effect}_{filename}")
                    
                    processed.save(new_path)
                    print(f" [V] Done! Saved as {os.path.basename(new_path)}")
            else:
                print(" [!] File missing.")

        except Exception as e:
            print(f" [!] Error: {e}")