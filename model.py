import pandas as pd
from prophet import Prophet
from prophet.serialize import model_to_json, model_from_json
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error
import joblib
import os
import json

MODEL_DIR = "models"
os.makedirs(MODEL_DIR, exist_ok=True)

def train_models(df):
    # df columns: timestamp, wait_minutes, temp, is_weekend, hour
    df = df.sort_values("timestamp")

    # Prophet training
    p_df = df[["timestamp", "wait_minutes"]].rename(columns={"timestamp": "ds", "wait_minutes": "y"})
    m = Prophet()
    m.fit(p_df)

    # Save Prophet model as JSON
    with open(os.path.join(MODEL_DIR, "prophet_model.json"), "w") as f:
        json.dump(model_to_json(m), f)

    # XGBoost training
    feature_cols = ["temp", "is_weekend", "hour"]
    xgb = XGBRegressor(n_estimators=200, max_depth=5, random_state=42)
    xgb.fit(df[feature_cols], df["wait_minutes"])
    joblib.dump(xgb, os.path.join(MODEL_DIR, "xgb.pkl"))

    pred = xgb.predict(df[feature_cols])
    mae = mean_absolute_error(df["wait_minutes"], pred)
    return mae

def predict_wait(features):
    with open(os.path.join(MODEL_DIR, "prophet_model.json"), "r") as f:
        prophet_model = model_from_json(json.load(f))  # Load Prophet model from JSON

    xgb = joblib.load(os.path.join(MODEL_DIR, "xgb.pkl"))

    # Prophet prediction (next hour)
    future = prophet_model.make_future_dataframe(periods=1, freq="H")
    ph_pred = prophet_model.predict(future).iloc[-1]["yhat"]

    xgb_pred = xgb.predict([[features["temp"], features["is_weekend"], features["hour"]]])[0]

    return float((ph_pred + xgb_pred) / 2)
