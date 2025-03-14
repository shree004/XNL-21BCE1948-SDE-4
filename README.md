# 🚀 Financial Transaction Fraud Detection API

A Flask-based API that predicts whether a financial transaction is fraudulent based on user input.

## 📌 Features
- Accepts JSON input with transaction details
- Uses a pre-trained **machine learning model** for fraud detection
- Supports **real-time predictions**
- Deployed on **Flask** with optional Nginx and Gunicorn for production

---

## 🛠 Setup Instructions

### 🔹 1. Clone the Repository
```bash
git clone https://github.com/yourusername/financial_transaction_system.git
cd financial_transaction_system
```

### 🔹 2. Create & Activate Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Linux/Mac
venv\Scripts\activate  # On Windows
```

### 🔹 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 🔹 4. Run the Flask API
```bash
python app.py
```
or for background execution:
```bash
nohup python app.py > logs.txt 2>&1 &
```

---

## 📡 API Endpoints

### 🔹 1. Predict Fraudulent Transactions
#### 🔗 Endpoint:  
```http
POST /predict
```
#### 📤 Request Body (JSON)
```json
{
  "user_id": 1,
  "amount": 1500.0,
  "location": "New York"
}
```
#### 📥 Response (JSON)
```json
{
  "is_fraud": true
}
```
or  
```json
{
  "is_fraud": false
}
```

---

## ⚙ Deployment Instructions

### 🔹 1. Run Flask on 0.0.0.0
Modify `app.py`:
```python
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
```

Then restart the server:
```bash
sudo kill -9 $(sudo lsof -t -i:5000)
nohup python app.py > logs.txt 2>&1 &
```

### 🔹 2. Open Firewall (if needed)
```bash
sudo ufw allow 5000/tcp
sudo ufw reload
```

### 🔹 3. Use Gunicorn for Production
```bash
pip install gunicorn
nohup gunicorn -w 4 -b 0.0.0.0:5000 app:app > logs.txt 2>&1 &
```

---

## 🛠 Troubleshooting

### 🔹 "Model or Scaler not loaded properly" Error
- Ensure `fraud_detection_model.pkl` and `scaler.pkl` exist:
  ```bash
  ls -lh fraud_detection_model.pkl scaler.pkl
  ```
- Verify files are not corrupted:
  ```python
  import pickle
  with open("fraud_detection_model.pkl", "rb") as f:
      model = pickle.load(f)
  with open("scaler.pkl", "rb") as f:
      scaler = pickle.load(f)
  print("Model and Scaler loaded successfully.")
  ```

### 🔹 Port 5000 is Already in Use
- Kill the running process:
  ```bash
  sudo kill -9 $(sudo lsof -t -i:5000)
  ```

---

## 📜 License

This project is licensed under the MIT License.
