import pandas as pd
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier

# Debug path
print(f"[📂] Current working directory: {os.getcwd()}")

# Load the preprocessed dataset
try:
    df = pd.read_csv("cleaned_articles.csv", encoding='utf-8-sig')
except FileNotFoundError:
    print("[❌] cleaned_articles.csv not found!")
    exit()

# Features and labels
X = df['text']
y = df['genre']

# Vectorize text
vectorizer = TfidfVectorizer(max_features=5000)
X_vec = vectorizer.fit_transform(X)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X_vec, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save model and vectorizer
try:
    joblib.dump(model, "model.pkl")
    joblib.dump(vectorizer, "vectorizer.pkl")
    print("[✅] Model and vectorizer saved successfully.")
except Exception as e:
    print(f"[❌] Failed to save model/vectorizer: {e}")
