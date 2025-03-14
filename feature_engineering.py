import pandas as pd
import numpy as np

# Load preprocessed transactions
try:
    df = pd.read_csv("preprocessed_transactions.csv")
    print(f"🔍 Loaded preprocessed data: {df.shape[0]} rows, {df.shape[1]} columns.")
except FileNotFoundError:
    print("❌ Error: `preprocessed_transactions.csv` not found! Run preprocessing.py first.")
    exit()

# If preprocessed data is empty, stop the script
if df.empty:
    print("❌ Error: The preprocessed dataset is empty! Check preprocessing.")
    exit()

# Feature engineering: Extract time-based features
df['timestamp'] = pd.to_datetime(df['timestamp'])
df['hour'] = df['timestamp'].dt.hour
df['day'] = df['timestamp'].dt.day
df['weekday'] = df['timestamp'].dt.weekday

# User-based aggregations
if 'user_id' in df.columns:
    df['user_transaction_count'] = df.groupby('user_id')['transaction_id'].transform('count')
    df['user_avg_amount'] = df.groupby('user_id')['amount'].transform('mean')
else:
    print("❌ Error: `user_id` column missing in preprocessed data!")

# Drop the timestamp column after feature extraction
df = df.drop(columns=['timestamp'], errors='ignore')

# Print the final dataframe preview
print(f"✅ Feature engineering complete! Processed {df.shape[0]} rows, {df.shape[1]} columns.")
print(df.head())  # Debugging output

# Save engineered dataset
df.to_csv("engineered_transactions.csv", index=False)

