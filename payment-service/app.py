from flask import Flask, request
import psycopg2

app = Flask(__name__)

# 🔴 Intentionally hardcoded credentials (vulnerability)
DB_CONFIG = {
    "host": "postgres",
    "database": "payments",
    "user": "admin",
    "password": "password"
}

def get_connection():
    return psycopg2.connect(**DB_CONFIG)

@app.route("/")
def home():
    return "Payment Service Running (PostgreSQL)"

@app.route("/pay", methods=["POST"])
def pay():
    user = request.json["user"]
    amount = request.json["amount"]

    conn = get_connection()
    cursor = conn.cursor()

    # 🔴 SQL Injection vulnerability (intentional)
    query = f"INSERT INTO payments (username, amount) VALUES ('{user}', {amount})"
    print("Executing query:", query, flush=True)

    cursor.execute(query)
    conn.commit()

    cursor.close()
    conn.close()

    return "Payment processed"

@app.route("/history", methods=["GET"])
def history():
    print("=== /history endpoint HIT ===", flush=True)

    user = request.args.get("user")
    print("User param:", user, flush=True)

    conn = get_connection()
    cursor = conn.cursor()

    # 🔴 SQL Injection vulnerability
    query = f"SELECT * FROM payments WHERE username = '{user}'"
    print("Executing query:", query, flush=True)

    cursor.execute(query)
    result = cursor.fetchall()

    cursor.close()
    conn.close()

    return str(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
