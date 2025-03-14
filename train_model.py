import pandas as pd
import numpy as np
import joblib
from collections import Counter
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# 🔹 Load dataset
df = pd.read_csv("preprocessed_transactions.csv")
print(f"🔍 Loaded dataset with {df.shape[0]} rows and {df.shape[1]} columns.")

# 🔹 Handle missing values (drop or fill)
df.dropna(inplace=True)  # Drop rows with missing values

# 🔹 Fix Class Label Issues
df["is_fraud"] = df["is_fraud"].astype(str).str.strip()  # Remove extra spaces
df["is_fraud"] = df["is_fraud"].map({"True": 1, "False": 0})  # Convert to binary

# 🔹 Check class distribution
class_counts = Counter(df["is_fraud"])
print(f"📊 Class distribution: {class_counts}")

# 🔹 Encode categorical features (e.g., location)
label_encoder = LabelEncoder()
if "location" in df.columns:
    df["location"] = label_encoder.fit_transform(df["location"])
else:
    label_encoder = None  # No categorical encoding needed

# 🔹 Define Features (X) & Target (y)
drop_columns = ["is_fraud", "transaction_id", "timestamp"]
X = df.drop(columns=[col for col in drop_columns if col in df.columns])  # Features
y = df["is_fraud"]  # Target variable

# 🔹 Standardize numerical features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 🔹 Train-Test Split (with Stratification)
if min(class_counts.values()) >= 2:  # Ensure at least 2 fraud cases for stratification
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=0.2, random_state=42, stratify=y
    )
else:
    print("⚠️ Not enough fraud cases for stratified splitting. Using random split.")
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

print(f"✅ Training set: {Counter(y_train)}, Test set: {Counter(y_test)}")
print("Features used for training:", X.columns.tolist())

# 🔹 Train RandomForest Classifier
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 🔹 Predictions & Evaluation
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"✅ Model Accuracy: {accuracy:.4f}")

print("\n📊 Classification Report:")
print(classification_report(y_test, y_pred, zero_division=1))  # Avoid division errors

# 🔹 Save Model & Preprocessors
joblib.dump(model, "fraud_detection_model.pkl")
joblib.dump(scaler, "scaler.pkl")
if label_encoder:
    joblib.dump(label_encoder, "label_encoder.pkl")

print("✅ Model, scaler, and label encoder (if used) saved successfully!")

