import os
import pandas as pd
import numpy as np
import random
from PIL import Image

dirs = [
    'backend/routes',
    'backend/services',
    'models',
    'data',
    'images/fashion',
    'saved_models',
    'tests',
]

for d in dirs:
    os.makedirs(d, exist_ok=True)

# Generate sample dataset
categories = ['T-shirt', 'Shirt', 'Jeans', 'Trousers', 'Jacket', 'Dress', 'Skirt', 'Shoes', 'Accessories']
colors = ['Black', 'White', 'Blue', 'Red', 'Green', 'Yellow', 'Grey', 'Brown']
styles = ['Casual', 'Formal', 'Sporty', 'Party', 'Vintage', 'Streetwear']
occasions = ['College', 'Office', 'Party', 'Gym', 'Wedding', 'Vacation']
seasons = ['Summer', 'Winter', 'All Season', 'Monsoon']
genders = ['Men', 'Women', 'Unisex']

items = []
for i in range(1, 101):
    cat = random.choice(categories)
    color = random.choice(colors)
    gender = 'Men' if cat in ['Shirt'] and random.random() < 0.7 else random.choice(genders)
    
    # Generate simple solid color image
    img = Image.new('RGB', (100, 100), color=color)
    img_path = f'images/fashion/item_{i}.jpg'
    img.save(img_path)

    items.append({
        'item_id': i,
        'item_name': f"{color} {cat} - {random.choice(styles)}",
        'category': cat,
        'subcategory': f"{cat}s",
        'color': color,
        'style': random.choice(styles),
        'occasion': random.choice(occasions),
        'season': random.choice(seasons),
        'gender': gender,
        'price': random.randint(500, 5000),
        'rating': round(random.uniform(3.0, 5.0), 1),
        'image_path': img_path
    })

df = pd.DataFrame(items)
df.to_csv('data/fashion_items.csv', index=False)

# Generate some dummy users
users = []
for i in range(1, 6):
    users.append({
        'user_id': i,
        'preferred_categories': 'T-shirt,Jeans,Shoes',
        'preferred_colors': 'Black,White,Blue',
        'preferred_styles': 'Casual,Streetwear',
        'preferred_occasions': 'College,Party',
        'budget_min': 1000,
        'budget_max': 5000,
        'liked_items': '1,5,12',
        'disliked_items': '2,3'
    })
df_users = pd.DataFrame(users)
df_users.to_csv('data/users.csv', index=False)

print("Scaffolding complete.")
