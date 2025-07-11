import pandas as pd
import numpy as np
import joblib
import os

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_absolute_error, r2_score

# Paths
yield_path = "data/combined_rice_data.csv"
npk_path = "data/combined_rice_data.csv"
encoder_path = "preprocessing/encoders.pkl"
model_path = "app/models/improved_yield_model.pkl"

# 1. Load datasets
df_yield = pd.read_csv(yield_path)
df_npk = pd.read_csv(npk_path)

# 2. Drop missing rows
df_yield.dropna(inplace=True)
df_npk.dropna(inplace=True)

# 3. Trim to equal length
min_len = min(len(df_yield), len(df_npk))
df_yield = df_yield.iloc[:min_len].copy()
df_npk = df_npk.iloc[:min_len].copy()

# 4. Label encode District
le = LabelEncoder()
df_yield["Dist Name"] = le.fit_transform(df_yield["Dist Name"])
joblib.dump(le, encoder_path)

# 5. Merge required columns
df = pd.DataFrame({
    "district": df_yield["Dist Name"],
    "year": df_yield["Year"],
    "production": df_yield["RICE PRODUCTION (1000 tons)"],
    "area": df_yield["RICE AREA (1000 ha)"],
    "yield": df_yield["RICE YIELD (Kg per ha)"],
    "rainfall": df_npk["rainfall"].values,
    "temperature": df_npk["temperature"].values,
    "humidity": df_npk["humidity"].values,
    "N": df_npk["N"].values,
    "P": df_npk["P"].values,
    "K": df_npk["K"].values
})

# 6. Feature engineering: prevent division by zero
df["prod_per_area"] = df["production"] / df["area"].replace(0, np.nan)

# 7. Handle infinite or missing values
df.replace([np.inf, -np.inf], np.nan, inplace=True)
df.dropna(inplace=True)

# 8. Define features & target
features = ["district", "year", "production", "area",
            "rainfall", "temperature", "humidity",
            "N", "P", "K", "prod_per_area"]

X = df[features]
y = df["yield"]

# 9. Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 10. Train RandomForestRegressor
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 11. Evaluate
y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f" Model trained successfully!")
print(f" MAE: {mae:.2f}")
print(f" R² Score: {r2:.4f}")

# 12. Save model
joblib.dump(model, model_path)
print(f" Model saved to: {model_path}")
