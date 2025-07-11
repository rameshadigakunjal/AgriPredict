import pandas as pd
import pickle
from sklearn.preprocessing import LabelEncoder

csv_path = 'data/combined_rice_data.csv'
df = pd.read_csv(csv_path)

# Use the correct column name for districts
districts = df['Dist Name'].unique()

district_encoder = LabelEncoder()
district_encoder.fit(districts)

with open('preprocessing/encoders.pkl', 'wb') as f:
    pickle.dump({'district': district_encoder}, f)

print("District encoder retrained and saved to preprocessing/encoders.pkl.")