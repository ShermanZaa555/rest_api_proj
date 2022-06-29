import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

def tts():
    df = pd.read_csv('../rest_api_proj/heart/data/processed data/heart_clean.csv')
    X, y = feature_target(df)
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)
    X_train_scaled, X_test_scaled = std_scaler(X_train, X_test)
    return X_train_scaled, X_test_scaled, y_train, y_test

def feature_target(df):
    X = df.drop('HeartDisease', axis=1)
    y = df['HeartDisease']
    return X, y

def std_scaler(X_train, X_test):
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    return X_train_scaled, X_test_scaled