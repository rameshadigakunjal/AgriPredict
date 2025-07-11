import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
import joblib

# Load dataset
DATA_PATH = "data/cleaned_rice_data.csv"
df = pd.read_csv(DATA_PATH)

# Feature selection
features = ["Year", "State Code", "Dist Name", "RICE AREA (1000 ha)", "RICE PRODUCTION (1000 tons)"]
target = "RICE YIELD (Kg per ha)"

# Encode district names
le = LabelEncoder()
df["Dist Name Encoded"] = le.fit_transform(df["Dist Name"])

X = df[["Year", "State Code", "Dist Name Encoded", "RICE AREA (1000 ha)", "RICE PRODUCTION (1000 tons)"]]
y = df[target]

# Train Random Forest
rf = RandomForestRegressor(n_estimators=100, random_state=42)
rf.fit(X, y)

# Save model and encoder
joblib.dump(rf, "app/models/random_forest_model.pkl")
joblib.dump(le, "preprocessing/district_encoder.pkl")
print("Random Forest model and encoder saved.")
