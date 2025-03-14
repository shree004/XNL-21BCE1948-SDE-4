import psycopg2

def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="fintech",
        user="fintech_user",
        password="securepassword"
    )

def insert_transaction(user_id, amount, transaction_type, merchant, location, is_fraudulent):
    try:
        conn = get_connection()
        cur = conn.cursor()

        query = """
        INSERT INTO transactions (user_id, amount, transaction_type, merchant, location, is_fraudulent)
        VALUES (%s, %s, %s, %s, %s, %s);
        """
        cur.execute(query, (user_id, amount, transaction_type, merchant, location, is_fraudulent))
        
        conn.commit()
        cur.close()
        conn.close()
        print("✅ Transaction added successfully!")

    except Exception as e:
        print("❌ Error:", e)

def fetch_transactions():
    try:
        conn = get_connection()
        cur = conn.cursor()
        
        cur.execute("SELECT * FROM transactions;")
        transactions = cur.fetchall()
        
        cur.close()
        conn.close()
        return transactions

    except Exception as e:
        print("❌ Error fetching transactions:", e)
        return []

# Test insert
if __name__ == "__main__":
    insert_transaction(5, 75.99, 'debit', 'Nike', 'London', False)
    print(fetch_transactions())
