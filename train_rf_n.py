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
target = "N"

X = df[features]
y = df[target]

rf_n = RandomForestRegressor(n_estimators=100, random_state=42)
rf_n.fit(X, y)

joblib.dump(rf_n, "app/models/rf_n.pkl")
print("Nitrogen (N) model saved.")
