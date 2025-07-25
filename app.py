from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
from datetime import datetime
from model import train_models, predict_wait
import requests

app = Flask(__name__)
CORS(app)

# Health check
@app.route("/")
def index():
    return "QueueSense Backend Running"

# POST /checkin: Add a check-in + weather info
@app.route('/checkin', methods=['POST'])
def checkin():
    data = request.get_json()
    place_id = data.get('place_id')
    wait_minutes = data.get('wait_minutes')

    # 🔑 Replace with your actual OpenWeatherMap API key
    weather_api_key = "0cedde5c4fdce3e3c4a288b88ec59659"
    location = "New York"  # Static for now

    try:
        weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={weather_api_key}&units=metric"
        response = requests.get(weather_url)
        response.raise_for_status()
        weather_data = response.json()

        temp_c = weather_data['main']['temp']
        condition = weather_data['weather'][0]['description']
        is_day = 1 if weather_data['weather'][0]['icon'].endswith('d') else 0

        conn = sqlite3.connect("data.db")
        c = conn.cursor()
        c.execute("""
            INSERT INTO checkins (place_id, wait_minutes, timestamp, temp_c, condition, is_day)
            VALUES (?, ?, datetime('now'), ?, ?, ?)
        """, (place_id, wait_minutes, temp_c, condition, is_day))
        conn.commit()
        conn.close()

        return jsonify({"ok": True})
    
    except Exception as e:
        return jsonify({"error": f"Weather API error: {str(e)}"}), 500

# POST /train: Train model
@app.route("/train", methods=["POST"])
def train():
    mae = train_models()
    return jsonify({"ok": True, "mae": round(mae, 2)})

# GET /predict: Predict wait time
@app.route("/predict")
def predict():
    place_id = request.args.get("place_id")
    prediction = predict_wait(place_id)
    return jsonify({"wait_minutes": prediction})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
