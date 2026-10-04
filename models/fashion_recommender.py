import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import joblib
import os
import cv2
from PIL import Image

class FashionRecommendationModel:
    def __init__(self, data_path='data/fashion_items.csv', users_path='data/users.csv'):
        self.data_path = data_path
        self.users_path = users_path
        self.items_df = None
        self.users_df = None
        self.tfidf = TfidfVectorizer(stop_words='english')
        self.tfidf_matrix = None
        self.content_similarity_matrix = None
        
        # Configuration for weights
        self.alpha = 0.5  # Content similarity weight
        self.beta = 0.3   # User preference weight
        self.gamma = 0.2  # Visual similarity weight

    def load_data(self):
        try:
            self.items_df = pd.read_csv(self.data_path)
            if os.path.exists(self.users_path):
                self.users_df = pd.read_csv(self.users_path)
            print("Data loaded successfully.")
        except Exception as e:
            print(f"Error loading data: {e}")

    def preprocess_data(self):
        # Combine text features for content-based recommendation
        self.items_df['text_features'] = self.items_df['category'].fillna('') + ' ' + \
                                         self.items_df['subcategory'].fillna('') + ' ' + \
                                         self.items_df['color'].fillna('') + ' ' + \
                                         self.items_df['style'].fillna('') + ' ' + \
                                         self.items_df['occasion'].fillna('') + ' ' + \
                                         self.items_df['season'].fillna('') + ' ' + \
                                         self.items_df['gender'].fillna('')
        self.items_df['text_features'] = self.items_df['text_features'].str.lower()
        print("Data preprocessed.")

    def build_feature_matrix(self):
        # TF-IDF on combined text features
        self.tfidf_matrix = self.tfidf.fit_transform(self.items_df['text_features'])
        print("Feature matrix created.")

    def calculate_similarity(self):
        # Cosine similarity for content
        self.content_similarity_matrix = cosine_similarity(self.tfidf_matrix, self.tfidf_matrix)
        print("Similarity matrix calculated.")

    def extract_visual_features(self, image_path):
        """Extract basic color histogram as visual feature"""
        try:
            if not os.path.exists(image_path):
                # Fallback zero vector
                return np.zeros(256 * 3)
            image = cv2.imread(image_path)
            if image is None:
                return np.zeros(256 * 3)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            hist = cv2.calcHist([image], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
            cv2.normalize(hist, hist)
            return hist.flatten()
        except Exception as e:
            return np.zeros(512)

    def calculate_visual_similarity(self, item1_idx, item2_idx):
        path1 = self.items_df.iloc[item1_idx]['image_path']
        path2 = self.items_df.iloc[item2_idx]['image_path']
        f1 = self.extract_visual_features(path1)
        f2 = self.extract_visual_features(path2)
        
        # Avoid division by zero
        norm1 = np.linalg.norm(f1)
        norm2 = np.linalg.norm(f2)
        if norm1 == 0 or norm2 == 0:
            return 0.0
            
        similarity = np.dot(f1, f2) / (norm1 * norm2)
        return similarity

    def create_user_profile(self, user_preferences):
        # user_preferences: dict with 'category', 'color', 'style', 'occasion', 'budget'
        pref_text = f"{user_preferences.get('category', '')} " \
                    f"{user_preferences.get('color', '')} " \
                    f"{user_preferences.get('style', '')} " \
                    f"{user_preferences.get('occasion', '')}".lower()
        pref_vector = self.tfidf.transform([pref_text])
        return pref_vector

    def calculate_personalization_score(self, pref_vector):
        # Similarity of all items with user preferences
        scores = cosine_similarity(pref_vector, self.tfidf_matrix).flatten()
        return scores

    def recommend_items(self, user_preferences, top_n=10):
        if self.items_df is None or self.tfidf_matrix is None:
            self.load_model()
            
        pref_text = f"{user_preferences.get('category', '')} " \
                    f"{user_preferences.get('color', '')} " \
                    f"{user_preferences.get('style', '')} " \
                    f"{user_preferences.get('occasion', '')}".lower()
        if pref_text.strip():
            pref_vector = self.tfidf.transform([pref_text])
            content_scores = self.calculate_personalization_score(pref_vector)
        else:
            content_scores = np.ones(len(self.items_df)) * 0.5
            
        valid_items = self.items_df.copy()
        
        pref_gender = user_preferences.get('gender', '')
        if pref_gender and pref_gender != 'Any':
            valid_items = valid_items[valid_items['gender'].isin([pref_gender, 'Unisex'])]
            
        budget = user_preferences.get('budget', None)
        if budget:
            valid_items = valid_items[valid_items['price'] <= float(budget)]
            
        # 0.4 Content Similarity + 0.3 Preference Score... Here we use content_scores as a proxy for Preference Match 
        # since it's the similarity between user input text and item features. 
        # We multiply by 100 to get a score between 0 and 100.
        valid_items['recommendation_score'] = content_scores[valid_items.index] * 100
        recommendations = valid_items.sort_values(by='recommendation_score', ascending=False).head(top_n)
        
        return recommendations.to_dict('records')

    def color_compatibility(self, c1, c2):
        c1, c2 = str(c1).lower(), str(c2).lower()
        if c1 == c2: return 0.8
        neutrals = ['black', 'white', 'grey', 'beige', 'navy']
        if c1 in neutrals or c2 in neutrals: return 1.0
        
        mapping = {
            'black': ['white', 'blue', 'grey', 'beige'],
            'white': ['black', 'blue', 'grey', 'navy'],
            'blue': ['white', 'black', 'grey', 'beige'],
            'grey': ['black', 'white', 'blue'],
            'beige': ['white', 'black', 'brown', 'navy']
        }
        if c1 in mapping and c2 in mapping[c1]: return 1.0
        if c2 in mapping and c1 in mapping[c2]: return 1.0
        return 0.5

    def generate_outfit(self, user_preferences):
        if self.items_df is None:
            self.load_model()
            
        filtered_df = self.items_df.copy()
        pref_gender = user_preferences.get('gender', '')
        if pref_gender and pref_gender != 'Any':
            filtered_df = filtered_df[filtered_df['gender'].isin([pref_gender, 'Unisex'])]
            
        budget = user_preferences.get('budget', float('inf'))
        budget = budget if budget else float('inf')
        
        pref_text = f"{user_preferences.get('category', '')} " \
                    f"{user_preferences.get('color', '')} " \
                    f"{user_preferences.get('style', '')} " \
                    f"{user_preferences.get('occasion', '')}".lower()
        if pref_text.strip():
            pref_vector = self.tfidf.transform([pref_text])
            content_scores = cosine_similarity(pref_vector, self.tfidf_matrix).flatten()
        else:
            content_scores = np.ones(len(self.items_df)) * 0.5
            
        filtered_df['pers_score'] = content_scores[filtered_df.index]
        
        top_cats = ['T-shirt', 'Shirt', 'Jacket', 'Top', 'Dress']
        bottom_cats = ['Jeans', 'Trousers', 'Skirt', 'Bottom']
        shoe_cats = ['Shoes', 'Footwear']
        acc_cats = ['Accessories', 'Accessory', 'Watch', 'Belt', 'Hat']
        
        tops_df = filtered_df[filtered_df['category'].isin(top_cats) | filtered_df['subcategory'].isin(top_cats)]
        bottoms_df = filtered_df[filtered_df['category'].isin(bottom_cats) | filtered_df['subcategory'].isin(bottom_cats)]
        shoes_df = filtered_df[filtered_df['category'].isin(shoe_cats) | filtered_df['subcategory'].isin(shoe_cats)]
        acc_df = filtered_df[filtered_df['category'].isin(acc_cats) | filtered_df['subcategory'].isin(acc_cats)]
        
        if tops_df.empty: tops_df = self.items_df[self.items_df['category'].isin(top_cats)]
        if bottoms_df.empty: bottoms_df = self.items_df[self.items_df['category'].isin(bottom_cats)]
        if shoes_df.empty: shoes_df = self.items_df[self.items_df['category'].isin(shoe_cats)]
        if acc_df.empty: acc_df = self.items_df[self.items_df['category'].isin(acc_cats)]
        
        import random
        # Sample for variety when regenerating
        t_sample = tops_df.nlargest(15, 'pers_score').to_dict('records')
        b_sample = bottoms_df.nlargest(15, 'pers_score').to_dict('records')
        s_sample = shoes_df.nlargest(15, 'pers_score').to_dict('records')
        a_sample = acc_df.nlargest(15, 'pers_score').to_dict('records')
        
        random.shuffle(t_sample)
        random.shuffle(b_sample)
        random.shuffle(s_sample)
        random.shuffle(a_sample)
        
        t_sample = t_sample[:4]
        b_sample = b_sample[:4]
        s_sample = s_sample[:4]
        a_sample = a_sample[:2]
        
        best_outfit = None
        best_score = -1
        
        # If no bottoms (e.g. they chose a Dress), just use an empty dict for bottom
        if not b_sample:
            b_sample = [{}]
            
        for t in t_sample:
            for b in b_sample:
                for s in s_sample:
                    for a in (a_sample if a_sample else [{}]):
                        total_price = t.get('price', 0) + b.get('price', 0) + s.get('price', 0) + a.get('price', 0)
                        
                        budget_score = 1.0 if total_price <= budget else 0.3
                        
                        occ_pref = user_preferences.get('occasion', '')
                        occ_score = 0.0
                        if occ_pref and occ_pref != 'Any':
                            matches = (t.get('occasion') == occ_pref) + (b.get('occasion') == occ_pref) + (s.get('occasion') == occ_pref)
                            occ_score = matches / 3.0 if b else (matches / 2.0)
                        else:
                            occ_score = 1.0 if (t.get('occasion') == s.get('occasion')) else 0.5
                            
                        style_pref = user_preferences.get('style', '')
                        style_score = 0.0
                        if style_pref and style_pref != 'Any':
                            matches = (t.get('style') == style_pref) + (b.get('style') == style_pref) + (s.get('style') == style_pref)
                            style_score = matches / 3.0 if b else (matches / 2.0)
                        else:
                            style_score = 1.0 if (t.get('style') == s.get('style')) else 0.5
                            
                        col_score = (self.color_compatibility(t.get('color'), b.get('color')) + self.color_compatibility(b.get('color'), s.get('color'))) / 2.0 if b else self.color_compatibility(t.get('color'), s.get('color'))
                        
                        compat_score = (occ_score + style_score + col_score) / 3.0
                        pers_score = (t.get('pers_score', 0) + b.get('pers_score', 0) + s.get('pers_score', 0)) / 3.0 if b else (t.get('pers_score', 0) + s.get('pers_score', 0)) / 2.0
                        
                        outfit_score = (compat_score * 0.4) + (pers_score * 0.4) + (budget_score * 0.2)
                        
                        if outfit_score > best_score:
                            best_score = outfit_score
                            best_outfit = {
                                'top': t,
                                'bottom': b,
                                'shoes': s,
                                'accessory': a,
                                'compatibility_score': round(max(50, compat_score * 100), 1),
                                'personalization_score': round(max(50, pers_score * 100), 1),
                                'total_price': total_price
                            }
                            
        return best_outfit

    def save_model(self, path='saved_models/model.pkl'):
        model_data = {
            'tfidf': self.tfidf,
            'tfidf_matrix': self.tfidf_matrix,
            'content_similarity_matrix': self.content_similarity_matrix,
            'items_df': self.items_df
        }
        joblib.dump(model_data, path)
        print("Model saved successfully.")

    def load_model(self, path='saved_models/model.pkl'):
        if os.path.exists(path):
            model_data = joblib.load(path)
            self.tfidf = model_data['tfidf']
            self.tfidf_matrix = model_data['tfidf_matrix']
            self.content_similarity_matrix = model_data['content_similarity_matrix']
            self.items_df = model_data['items_df']
            print("Model loaded successfully.")
        else:
            print("Saved model not found. Rebuilding model...")
            self.load_data()
            self.preprocess_data()
            self.build_feature_matrix()
            self.calculate_similarity()
            self.save_model(path)
