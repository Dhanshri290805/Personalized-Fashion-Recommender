import os
from PIL import Image, ImageDraw, ImageFont
import uuid

class OutfitImageGenerator:
    def __init__(self, output_dir="generated_outfits"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        
    def generate_outfit_image(self, top_image_path, bottom_image_path, shoes_image_path, accessory_image_path=None, outfit_id=None):
        if not outfit_id:
            outfit_id = str(uuid.uuid4())[:8]
            
        width = 800
        height = 1000
        
        outfit_img = Image.new('RGB', (width, height), color='white')
        draw = ImageDraw.Draw(outfit_img)
        
        try:
            font_title = ImageFont.truetype("arial.ttf", 36)
            font_label = ImageFont.truetype("arial.ttf", 24)
        except:
            font_title = ImageFont.load_default()
            font_label = ImageFont.load_default()
            
        title = "PERSONALIZED OUTFIT"
        
        try:
            bbox = draw.textbbox((0, 0), title, font=font_title)
            title_w = bbox[2] - bbox[0]
        except AttributeError:
            title_w = font_title.getsize(title)[0]
            
        draw.text(((width - title_w) // 2, 30), title, fill="black", font=font_title)
        
        def paste_image(path, label, box, label_pos, max_size):
            if path and os.path.exists(path):
                try:
                    img = Image.open(path)
                    img.thumbnail(max_size, Image.Resampling.LANCZOS)
                    paste_x = box[0] + (max_size[0] - img.width) // 2
                    paste_y = box[1] + (max_size[1] - img.height) // 2
                    outfit_img.paste(img, (paste_x, paste_y))
                    
                    try:
                        bbox = draw.textbbox((0, 0), label, font=font_label)
                        label_w = bbox[2] - bbox[0]
                    except AttributeError:
                        label_w = font_label.getsize(label)[0]
                        
                    draw.text((box[0] + (max_size[0] - label_w) // 2, label_pos[1]), label, fill="black", font=font_label)
                except Exception as e:
                    print(f"Error pasting {label} image: {e}")
            else:
                draw.text(label_pos, f"[Missing {label} Image]", fill="red", font=font_label)

        paste_image(top_image_path, "TOP", (250, 120), (0, 90), (300, 300))
        paste_image(bottom_image_path, "BOTTOM", (250, 460), (0, 430), (300, 300))
        paste_image(shoes_image_path, "SHOES", (100, 770), (0, 740), (250, 200))
        paste_image(accessory_image_path, "ACCESSORY", (450, 770), (0, 740), (250, 200))
        
        # Connectors
        draw.line([(400, 420), (400, 450)], fill="black", width=2)
        draw.line([(400, 760), (400, 780)], fill="black", width=2)
        draw.line([(225, 780), (575, 780)], fill="black", width=2)
        draw.line([(225, 780), (225, 800)], fill="black", width=2)
        draw.line([(575, 780), (575, 800)], fill="black", width=2)
        
        filename = f"outfit_{outfit_id}.png"
        output_path = os.path.join(self.output_dir, filename)
        outfit_img.save(output_path)
        
        return f"/generated_outfits/{filename}"
