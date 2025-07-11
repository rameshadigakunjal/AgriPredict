import pandas as pd
import numpy as np
import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_absolute_error, r2_score

# Load dataset
csv_path = 'data/combined_rice_data.csv'
df = pd.read_csv(csv_path)

# Drop missing rows
cols_needed = ['Dist Name', 'Year', 'RICE AREA (1000 ha)', 'RICE PRODUCTION (1000 tons)', 'temperature', 'rainfall', 'humidity', 'RICE YIELD (Kg per ha)', 'N', 'P', 'K']
df = df[cols_needed].dropna()

# Encode district
le = LabelEncoder()
df['district_encoded'] = le.fit_transform(df['Dist Name'])
joblib.dump(le, 'preprocessing/district_encoder_combined.pkl')

# Features and targets
features = ['district_encoded', 'Year', 'RICE AREA (1000 ha)', 'RICE PRODUCTION (1000 tons)', 'temperature', 'rainfall', 'humidity']
X = df[features]

y_yield = df['RICE YIELD (Kg per ha)']
y_n = df['N']
y_p = df['P']
y_k = df['K']

# Train/test split
X_train, X_test, y_yield_train, y_yield_test = train_test_split(X, y_yield, test_size=0.2, random_state=42)
_, _, y_n_train, y_n_test = train_test_split(X, y_n, test_size=0.2, random_state=42)
_, _, y_p_train, y_p_test = train_test_split(X, y_p, test_size=0.2, random_state=42)
_, _, y_k_train, y_k_test = train_test_split(X, y_k, test_size=0.2, random_state=42)

# Train models
rf_yield = RandomForestRegressor(n_estimators=100, random_state=42)
rf_n = RandomForestRegressor(n_estimators=100, random_state=42)
rf_p = RandomForestRegressor(n_estimators=100, random_state=42)
rf_k = RandomForestRegressor(n_estimators=100, random_state=42)

rf_yield.fit(X_train, y_yield_train)
rf_n.fit(X_train, y_n_train)
rf_p.fit(X_train, y_p_train)
rf_k.fit(X_train, y_k_train)

# Save models
joblib.dump(rf_yield, 'app/models/rf_yield.pkl')
joblib.dump(rf_n, 'app/models/rf_n.pkl')
joblib.dump(rf_p, 'app/models/rf_p.pkl')
joblib.dump(rf_k, 'app/models/rf_k.pkl')

print('Models trained and saved.')
