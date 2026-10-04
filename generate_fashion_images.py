import os
import pandas as pd
from PIL import Image, ImageDraw, ImageFont

def get_color_rgb(color_name):
    colors = {
        'black': (30, 30, 30),
        'white': (245, 245, 245),
        'red': (220, 50, 50),
        'blue': (50, 100, 220),
        'yellow': (240, 220, 50),
        'brown': (139, 69, 19),
        'grey': (128, 128, 128),
        'navy': (0, 0, 128),
        'beige': (245, 245, 220),
        'silver': (192, 192, 192),
        'gold': (255, 215, 0),
        'green': (34, 139, 34)
    }
    return colors.get(str(color_name).lower(), (200, 200, 200))

def draw_tshirt(draw, color, width, height):
    body = [(width*0.3, height*0.2), (width*0.7, height*0.2), 
            (width*0.7, height*0.8), (width*0.3, height*0.8)]
    sleeve_l = [(width*0.3, height*0.2), (width*0.1, height*0.4), (width*0.2, height*0.5), (width*0.3, height*0.4)]
    sleeve_r = [(width*0.7, height*0.2), (width*0.9, height*0.4), (width*0.8, height*0.5), (width*0.7, height*0.4)]
    neck = [(width*0.4, height*0.2), (width*0.6, height*0.2), (width*0.5, height*0.3)]
    
    draw.polygon(body, fill=color)
    draw.polygon(sleeve_l, fill=color)
    draw.polygon(sleeve_r, fill=color)
    draw.polygon(neck, fill=(255,255,255))

def draw_jeans(draw, color, width, height):
    waist = [(width*0.3, height*0.2), (width*0.7, height*0.2),
             (width*0.7, height*0.4), (width*0.3, height*0.4)]
    leg_l = [(width*0.3, height*0.4), (width*0.45, height*0.4), (width*0.45, height*0.9), (width*0.3, height*0.9)]
    leg_r = [(width*0.55, height*0.4), (width*0.7, height*0.4), (width*0.7, height*0.9), (width*0.55, height*0.9)]
    
    draw.polygon(waist, fill=color)
    draw.polygon(leg_l, fill=color)
    draw.polygon(leg_r, fill=color)

def draw_dress(draw, color, width, height):
    top = [(width*0.35, height*0.1), (width*0.65, height*0.1), (width*0.6, height*0.4), (width*0.4, height*0.4)]
    skirt = [(width*0.4, height*0.4), (width*0.6, height*0.4), (width*0.8, height*0.9), (width*0.2, height*0.9)]
    draw.polygon(top, fill=color)
    draw.polygon(skirt, fill=color)

def draw_shoes(draw, color, width, height):
    shoe_l = [(width*0.2, height*0.7), (width*0.4, height*0.7), (width*0.45, height*0.85), (width*0.15, height*0.85)]
    shoe_r = [(width*0.6, height*0.7), (width*0.8, height*0.7), (width*0.85, height*0.85), (width*0.55, height*0.85)]
    draw.polygon(shoe_l, fill=color)
    draw.polygon(shoe_r, fill=color)

def draw_accessory(draw, color, width, height):
    draw.ellipse([(width*0.3, height*0.3), (width*0.7, height*0.7)], fill=color)
    draw.ellipse([(width*0.4, height*0.4), (width*0.6, height*0.6)], fill=(255,255,255))

def generate_image(category, color_name, save_path):
    width, height = 400, 400
    img = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(img)
    
    color = get_color_rgb(color_name)
    cat_lower = str(category).lower()
    
    if 't-shirt' in cat_lower or 'shirt' in cat_lower or 'top' in cat_lower:
        draw_tshirt(draw, color, width, height)
    elif 'jeans' in cat_lower or 'trouser' in cat_lower or 'bottom' in cat_lower or 'skirt' in cat_lower:
        draw_jeans(draw, color, width, height)
    elif 'dress' in cat_lower:
        draw_dress(draw, color, width, height)
    elif 'shoe' in cat_lower or 'footwear' in cat_lower:
        draw_shoes(draw, color, width, height)
    else:
        draw_accessory(draw, color, width, height)
    
    try:
        font = ImageFont.truetype("arial.ttf", 20)
    except:
        font = ImageFont.load_default()
        
    text = f"{str(color_name).capitalize()} {str(category).capitalize()}"
    try:
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
    except AttributeError:
        # Fallback for older Pillow versions
        text_width = font.getsize(text)[0]
        
    draw.text(((width - text_width) / 2, height - 30), text, fill="black", font=font)
    
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    img.save(save_path)

def generate_all_images():
    print("Generating fashion images...")
    df = pd.read_csv('data/fashion_items.csv')
    count = 0
    for idx, row in df.iterrows():
        path = row['image_path']
        if not os.path.exists(path):
            generate_image(row['category'], row['color'], path)
            print(f"[{idx+1}/{len(df)}] {row['item_name']} \u2713")
        count += 1
    print(f"{count} fashion images ready.")

if __name__ == "__main__":
    generate_all_images()
