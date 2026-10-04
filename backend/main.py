from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from backend.routes import recommendation_routes
import os

app = FastAPI(title="Personalized Clothing & Fashion Recommendation System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure images directory exists before mounting
os.makedirs("images/fashion", exist_ok=True)
os.makedirs("generated_outfits", exist_ok=True)

app.mount("/images", StaticFiles(directory="images"), name="images")
app.mount("/generated_outfits", StaticFiles(directory="generated_outfits"), name="generated_outfits")

app.include_router(recommendation_routes.router, prefix="/api")

@app.get("/api/health")
def health_check():
    return {
        "status": "ok",
        "model": "fashion-recommender"
    }
