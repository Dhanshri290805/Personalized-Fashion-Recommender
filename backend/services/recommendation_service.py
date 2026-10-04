from models.fashion_recommender import FashionRecommendationModel
from backend.services.outfit_image_generator import OutfitImageGenerator

model_instance = FashionRecommendationModel()
model_instance.load_model('saved_models/model.pkl')
image_generator = OutfitImageGenerator()

def get_recommendations(preferences, top_n=10):
    recs = model_instance.recommend_items(preferences, top_n)
    return recs

def get_outfit(preferences):
    outfit = model_instance.generate_outfit(preferences)
    if outfit:
        top_img = outfit.get('top', {}).get('image_path')
        bottom_img = outfit.get('bottom', {}).get('image_path')
        shoes_img = outfit.get('shoes', {}).get('image_path')
        acc_img = outfit.get('accessory', {}).get('image_path')
        
        # Ensure we pass absolute or correct relative paths. Assuming they are relative to current dir
        outfit_img_url = image_generator.generate_outfit_image(
            top_image_path=top_img,
            bottom_image_path=bottom_img,
            shoes_image_path=shoes_img,
            accessory_image_path=acc_img
        )
        outfit['outfit_image'] = outfit_img_url
        
    return outfit

def get_all_items():
    if model_instance.items_df is not None:
        return model_instance.items_df.to_dict('records')
    return []

def process_feedback(item_id, user_id, feedback_type):
    # In a real app, save this to DB to re-train the model.
    # For demo, just return success.
    print(f"Feedback received: User {user_id} {feedback_type} item {item_id}")
    return {"status": "success", "message": "Feedback recorded."}
