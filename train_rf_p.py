import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
import joblib

df = pd.read_csv("data/combined_rice_data.csv")
le = LabelEncoder()
df["Dist Name Encoded"] = le.fit_transform(df["Dist Name"])

features = [
    "Dist Name Encoded", "Year", "Dist Code", "State Code", "RICE AREA (1000 ha)",
    "RICE PRODUCTION (1000 tons)", "temperature", "humidity", "rainfall"
]
target = "P"

X = df[features]
y = df[target]

rf_p = RandomForestRegressor(n_estimators=100, random_state=42)
rf_p.fit(X, y)

joblib.dump(rf_p, "app/models/rf_p.pkl")
print("Phosphorus (P) model saved.")
