from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import os

# Check for model files
if not os.path.exists("model.pkl") or not os.path.exists("vectorizer.pkl"):
    raise FileNotFoundError("model.pkl or vectorizer.pkl not found. Run train_model.py first.")

# Load model and vectorizer
model = joblib.load("model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

# FastAPI app
app = FastAPI(title="News Genre Classifier API")

# Data model
class Article(BaseModel):
    headline: str
    article: str

# Root route
@app.get("/")
def read_root():
    return {"message": "Welcome to the News Genre Classifier API!"}

# Prediction route
@app.post("/predict")
def predict_genre(data: Article):
    text = data.headline + " " + data.article
    vec = vectorizer.transform([text])
    prediction = model.predict(vec)[0]
    return {"genre": prediction}
