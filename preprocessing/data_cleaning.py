# preprocessing/data_cleaning.py

import pandas as pd
from sklearn.preprocessing import LabelEncoder
import joblib
import os

def preprocess_p1(data_path):
    df = pd.read_csv(data_path)
    df.dropna(inplace=True)

    le = LabelEncoder()
    df['Dist Name'] = le.fit_transform(df['Dist Name'])
    joblib.dump(le, 'preprocessing/encoders.pkl')  # Save encoder

    X = df[['Dist Name', 'Year', 'RICE PRODUCTION (1000 tons)']]
    y = df['RICE YIELD (Kg per ha)']
    return X, y

def preprocess_p2(data_path):
    df = pd.read_csv(data_path)
    df.dropna(inplace=True)

    X = df[['rainfall', 'temperature', 'humidity']]
    y = df[['N', 'P', 'K']]
    return X, y
