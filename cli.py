import sys
import os

# Ensure we can import from models
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.fashion_recommender import FashionRecommendationModel

def main():
    print("=====================================================")
    print(" Personalized Clothing & Fashion Recommendation System ")
    print("=====================================================")
    
    print("\nLoading model... Please wait.")
    model = FashionRecommendationModel()
    model.load_model('saved_models/model.pkl')
    
    while True:
        print("\nWhat would you like to do?")
        print("1. Get Clothing Recommendations")
        print("2. Generate a Complete Outfit")
        print("3. Exit")
        
        choice = input("Enter your choice (1/2/3): ").strip()
        
        if choice == '3':
            print("Exiting... Have a stylish day!")
            break
        elif choice in ['1', '2']:
            print("\n--- Enter Your Preferences ---")
            gender = input("Gender (Men/Women/Unisex or leave blank for Any): ").strip()
            category = input("Preferred Category (T-shirt/Jeans/Shoes/etc. or leave blank): ").strip()
            color = input("Preferred Color (Black/White/Blue/etc. or leave blank): ").strip()
            style = input("Style (Casual/Formal/Party/etc. or leave blank): ").strip()
            occasion = input("Occasion (College/Office/Party/etc. or leave blank): ").strip()
            budget = input("Maximum Budget in INR (e.g. 3000 or leave blank): ").strip()
            
            prefs = {
                "gender": gender,
                "category": category,
                "color": color,
                "style": style,
                "occasion": occasion,
                "budget": float(budget) if budget.isdigit() else None
            }
            
            if choice == '1':
                print("\nFetching top recommendations...")
                recs = model.recommend_items(prefs, top_n=5)
                if not recs:
                    print("No items found matching your criteria.")
                else:
                    for i, item in enumerate(recs, 1):
                        print(f"{i}. {item['item_name']} | Category: {item['category']} | Style: {item['style']} | Price: ₹{item['price']}")
            
            elif choice == '2':
                print("\nGenerating your personalized outfit...")
                outfit = model.generate_outfit(prefs)
                
                print("\n--- Your Curated Outfit ---")
                if outfit.get('top') and outfit['top'].get('item_name'):
                    print(f"Top:       {outfit['top']['item_name']} (₹{outfit['top'].get('price', '')})")
                if outfit.get('bottom') and outfit['bottom'].get('item_name'):
                    print(f"Bottom:    {outfit['bottom']['item_name']} (₹{outfit['bottom'].get('price', '')})")
                if outfit.get('shoes') and outfit['shoes'].get('item_name'):
                    print(f"Shoes:     {outfit['shoes']['item_name']} (₹{outfit['shoes'].get('price', '')})")
                if outfit.get('accessory') and outfit['accessory'].get('item_name'):
                    print(f"Accessory: {outfit['accessory']['item_name']} (₹{outfit['accessory'].get('price', '')})")
                    
                print(f"\nCompatibility Score: {outfit.get('compatibility_score', 0)}%")
                print(f"Personalization Score: {outfit.get('personalization_score', 0)}%")
                if 'total_price' in outfit:
                    print(f"Total Price: ₹{outfit['total_price']}")
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()
