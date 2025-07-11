import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
import joblib

# Load dataset
DATA_PATH = "data/combined_rice_data.csv"
df = pd.read_csv(DATA_PATH)

# Encode district names
le = LabelEncoder()
df["Dist Name Encoded"] = le.fit_transform(df["Dist Name"])

features = [
    "Dist Name Encoded", "Year", "Dist Code", "State Code", "RICE AREA (1000 ha)",
    "RICE PRODUCTION (1000 tons)", "temperature", "humidity", "rainfall"
]

# Train and save N model
X_n = df[features]
y_n = df["N"]
rf_n = RandomForestRegressor(n_estimators=100, random_state=42)
rf_n.fit(X_n, y_n)
joblib.dump(rf_n, "app/models/rf_n.pkl")
print("Nitrogen (N) model saved.")

# Train and save P model
X_p = df[features]
y_p = df["P"]
rf_p = RandomForestRegressor(n_estimators=100, random_state=42)
rf_p.fit(X_p, y_p)
joblib.dump(rf_p, "app/models/rf_p.pkl")
print("Phosphorus (P) model saved.")

# Train and save K model
X_k = df[features]
y_k = df["K"]
rf_k = RandomForestRegressor(n_estimators=100, random_state=42)
rf_k.fit(X_k, y_k)
joblib.dump(rf_k, "app/models/rf_k.pkl")
print("Potassium (K) model saved.")

# Train and save pH model
X_ph = df[features]
y_ph = df["ph"]
rf_ph = RandomForestRegressor(n_estimators=100, random_state=42)
rf_ph.fit(X_ph, y_ph)
joblib.dump(rf_ph, "app/models/rf_ph.pkl")
print("pH model saved.")
