from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import joblib
import os

# Load model and vectorizer
if not os.path.exists("model.pkl") or not os.path.exists("vectorizer.pkl"):
    raise FileNotFoundError("model.pkl or vectorizer.pkl not found. Run train_model.py first.")
model = joblib.load("model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

# FastAPI app setup
app = FastAPI(title="News Genre Classifier UI")
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Home page
@app.get("/", response_class=HTMLResponse)
async def form_get(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "result": None})

# Handle form submission
@app.post("/", response_class=HTMLResponse)
async def form_post(request: Request, headline: str = Form(...), article: str = Form(...)):
    text = headline + " " + article
    vec = vectorizer.transform([text])
    prediction = model.predict(vec)[0]
    return templates.TemplateResponse("index.html", {"request": request, "result": prediction})
