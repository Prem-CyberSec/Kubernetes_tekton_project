from flask import Flask, request
import sqlite3

app = Flask(__name__)

def get_db():
    return sqlite3.connect("payments.db")

@app.route("/pay", methods=["POST"])
def pay():
    user = request.json["user"]
    amount = request.json["amount"]

    conn = get_db()
    cursor = conn.cursor()

    # SQL Injection Vulnerability
    query = f"INSERT INTO payments (user, amount) VALUES ('{user}', {amount})"
    cursor.execute(query)
    conn.commit()

    return "Payment processed"

@app.route("/history", methods=["GET"])
def history():
    user = request.args.get("user")

    conn = get_db()
    cursor = conn.cursor()

    # SQL Injection
    query = f"SELECT * FROM payments WHERE user = '{user}'"
    result = cursor.execute(query).fetchall()

    return str(result)

app.run(host="0.0.0.0", port=5001)
