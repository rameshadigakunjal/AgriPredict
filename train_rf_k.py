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
target = "K"

X = df[features]
y = df[target]

rf_k = RandomForestRegressor(n_estimators=100, random_state=42)
rf_k.fit(X, y)

joblib.dump(rf_k, "app/models/rf_k.pkl")
print("Potassium (K) model saved.")
