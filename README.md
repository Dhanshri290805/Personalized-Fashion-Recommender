# Personalized Fashion Recommender

**AI-Based Personalized Clothing & Outfit Recommendations**

## Overview
The Personalized Fashion Recommender is an AI-powered application that recommends personalized fashion items and generates compatible outfits based on user preferences. Users can specify their preferences, including:
* Gender
* Category
* Preferred Color
* Style
* Occasion
* Maximum Budget

Based on these inputs, the recommendation engine processes a local dataset of fashion items and ranks them using content-based filtering. The system can also combine individual clothing items (tops, bottoms, shoes, accessories) into cohesive, personalized outfits, factoring in budget, color compatibility, and occasion matching.

## Main Features
* Personalized fashion recommendation
* Clothing-item filtering
* Budget-aware recommendations
* Style and occasion matching
* Recommendation scoring
* Outfit generation
* Outfit compatibility scoring
* Personalized outfit scoring
* Actual clothing images
* Dynamic generated outfit images
* Like/Dislike feedback
* Regenerate Outfit functionality
* Local dataset
* Local image processing

## Technology Stack
* Python
* FastAPI
* React
* JavaScript
* Pandas
* NumPy
* Pillow
* HTML
* CSS

## Project Architecture
```text
User Preferences
       ↓
Recommendation Engine
       ↓
Fashion Dataset
       ↓
Personalized Ranking
       ↓
Compatible Outfit Selection
       ↓
Actual Clothing Images
       ↓
Outfit Image Generation
       ↓
Personalized Outfit
       ↓
User Feedback
```

## How to Run

### 1. Backend

Open a terminal and navigate to the project root directory:

```bash
cd backend
# Or from the project root simply activate the venv
..\venv\Scripts\activate
# If dependencies are missing, install them:
pip install -r ..\requirements.txt
# Start the FastAPI server
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```

### 2. Frontend

Open a separate terminal window and navigate to the `frontend` directory:

```bash
cd frontend
# Install dependencies
npm install
# Start the Vite development server
npm run dev
```

*(Alternatively, you can just double-click `run.bat` in the project root on Windows to automatically launch both servers.)*

## Project Structure
```text
Personalized-Fashion-Recommender/
│
├── backend/
│   ├── main.py
│   ├── routes/
│   └── services/
├── frontend/
│   ├── src/
│   ├── package.json
│   └── vite.config.js
├── data/
│   ├── fashion_items.csv
│   └── users.csv
├── images/
│   └── fashion/
├── generated_outfits/
├── models/
│   └── fashion_recommender.py
├── saved_models/
├── README.md
├── .gitignore
├── requirements.txt
├── run.bat
├── run_cli.bat
├── train.py
└── cli.py
```

## Development Attribution
This project was developed with the assistance of Antigravity, an AI-powered coding and development environment.

Antigravity was used to assist with project implementation, code generation, debugging, integration, testing, and development workflow.

Repository owner: Dhanshri Kubade
GitHub: Dhanshri290805
