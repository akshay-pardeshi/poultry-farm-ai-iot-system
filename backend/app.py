from flask import Flask, jsonify
from flask_cors import CORS
import utils
import threading
import time
import joblib
import numpy as np

app = Flask(__name__)
CORS(app)  # ✅ Allow cross-origin requests (important for React frontend)

# Load trained model and scaler
model = joblib.load('models/lstm_rf_model.pkl')
scaler = joblib.load('models/scaler.pkl')

# Map prediction output to labels
label_map = {0: "Healthy", 1: "Stressed", 2: "Sick"}

# Global variable to store latest sensor data and prediction
latest_data = {}

# 🔄 Update data in background every 5 seconds
def update_data():
    global latest_data
    while True:
        raw_data = utils.generate_sensor_data()
        latest_data = raw_data.copy()

        # ✅ Prepare input for prediction
        input_data = np.array([[  
            raw_data['temperature'], raw_data['humidity'],
            raw_data['nh3'], raw_data['weight'],
            raw_data['motion'], raw_data['age']
        ]])

        # 🔬 Scale and reshape for LSTM model
        scaled_input = scaler.transform(input_data)
        reshaped_input = scaled_input.reshape((scaled_input.shape[0], 1, scaled_input.shape[1]))
        prediction = model.predict(reshaped_input)

        # 🔁 Add prediction result to data
        latest_data['predicted_health'] = label_map.get(int(prediction[0]), "Unknown")

        time.sleep(5)

# 🌐 Homepage route
@app.route('/')
def home():
    return "✅ Poultry Farm Backend is Running"

# 📡 API endpoint to return latest data with health prediction
@app.route('/api/data', methods=['GET'])
def get_data():
    return jsonify(latest_data) 


# 🚀 Start Flask app and background thread
if __name__ == "__main__":
    thread = threading.Thread(target=update_data)
    thread.daemon = True
    thread.start()

    app.run(host='0.0.0.0', port=5000)
