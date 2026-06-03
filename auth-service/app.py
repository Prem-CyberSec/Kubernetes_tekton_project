from flask import Flask, request, jsonify
import jwt

app = Flask(__name__)
SECRET = "hardcoded-secret"  # Vulnerability

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    if data["username"] == "admin" and data["password"] == "password":
        token = jwt.encode({"user": "admin"}, SECRET, algorithm="HS256")
        return jsonify({"token": token})
    return "Unauthorized", 401

@app.route("/verify", methods=["GET"])
def verify():
    token = request.headers.get("Authorization")
    try:
        payload = jwt.decode(token, options={"verify_signature": False})  # Vulnerability
        return jsonify(payload)
    except:
        return "Invalid token", 403

app.run(host="0.0.0.0", port=5000)
