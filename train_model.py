import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

# Load dataset
df = pd.read_csv("Crop_recommendation.csv")

# Features and target
X = df.drop("label", axis=1)
y = df["label"]

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# Save model
joblib.dump(model, "model.pkl")

print("model.pkl created successfully!")