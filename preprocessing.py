import pandas as pd
import numpy as np
import psycopg2
from sqlalchemy import create_engine

# PostgreSQL connection details
DB_CONFIG = {
    "dbname": "financial_db",
    "user": "fintech_user",
    "password": "shree",
    "host": "localhost",
    "port": "5432"
}

# Create a SQLAlchemy engine
engine = create_engine(f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['dbname']}")

# Connect to PostgreSQL
try:
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    print("✅ Connected to PostgreSQL")
except Exception as e:
    print(f"❌ Database Connection Error: {e}")
    exit()

# Load transactions
try:
    query = "SELECT transaction_id, user_id, amount, timestamp, location, is_fraud FROM transactions;"
    df = pd.read_sql_query(query, conn)
    print("✅ Transactions loaded successfully!")
except Exception as e:
    print(f"❌ Error loading transactions: {e}")
    conn.close()
    exit()

# Close the database connection
cursor.close()
conn.close()

# Handle missing values
df['amount']=df['amount'].fillna(df['amount'].median())
df['location']=df['location'].fillna('UNKNOWN')

# Handle outliers (Remove transactions above 99th percentile)
upper_limit = df['amount'].quantile(0.99)
df = df[df['amount'] <= upper_limit]
print(f"🔍 Loaded transactions shape: {df.shape}")

# Save preprocessed data
df.to_csv("preprocessed_transactions.csv", index=False)
print("✅ Preprocessed data saved as 'preprocessed_transactions.csv'")
