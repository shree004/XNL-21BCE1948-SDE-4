import joblib
import pandas as pd
from flask import Flask, request, jsonify
import numpy as np

# 🔹 Load trained model and preprocessing tools
model = joblib.load("fraud_detection_model.pkl")
scaler = joblib.load("scaler.pkl")

# 🔹 Load LabelEncoder correctly
try:
    label_encoder = joblib.load("label_encoder.pkl")
except FileNotFoundError:
    label_encoder = None  # If no encoding was needed during training

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        print("📥 Incoming data:", data)  # Debugging

        # 🔹 Convert input to DataFrame
        df = pd.DataFrame([data])

        # 🔹 Check if required columns exist
        required_columns = ["user_id", "amount", "location"]
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            return jsonify({"error": f"Missing columns: {', '.join(missing_columns)}"}), 400

        # 🔹 Encode location (if applicable)
        if label_encoder:
            if df["location"].iloc[0] not in label_encoder.classes_:
                return jsonify({"error": f"Unknown location: {df['location'].iloc[0]}"})
            df["location"] = label_encoder.transform([df["location"].iloc[0]])[0]

        # 🔹 Ensure correct feature order before scaling
        df = df[["user_id", "amount", "location"]]

        # 🔹 Scale numerical features
        df_scaled = scaler.transform(df)  # ✅ FIX: Use `joblib.load()` for correct scaler

        # 🔹 Predict fraud (convert NumPy boolean to Python bool)
        prediction = bool(model.predict(df_scaled)[0])

        return jsonify({"is_fraud": prediction})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

