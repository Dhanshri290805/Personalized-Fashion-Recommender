import os
from models.fashion_recommender import FashionRecommendationModel

def main():
    print("Starting Training Process...")
    model = FashionRecommendationModel()
    
    # 1. Load the dataset
    model.load_data()
    if model.items_df is not None:
        print(f"Number of items: {len(model.items_df)}")
    else:
        print("Failed to load dataset.")
        return

    # 2. Preprocess the data
    model.preprocess_data()
    
    # 3. Build features
    model.build_feature_matrix()
    
    # 4. Train/build the recommendation model (Calculate similarities)
    model.calculate_similarity()
    print("Recommendation model built successfully.")
    
    # 5. Save the required model artifacts
    os.makedirs('saved_models', exist_ok=True)
    model.save_model('saved_models/model.pkl')

if __name__ == "__main__":
    main()
