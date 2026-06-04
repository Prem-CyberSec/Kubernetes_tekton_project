from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Internal service URLs (Kubernetes DNS)
AUTH_SERVICE = "http://auth-service:5000"
PAYMENT_SERVICE = "http://payment-service:5001"

@app.route("/")
def home():
    return "API Gateway Running"

# ✅ LOGIN (proxy to auth service)
@app.route("/login", methods=["POST"])
def login():
    response = requests.post(f"{AUTH_SERVICE}/login", json=request.json)
    return response.text, response.status_code


# 🔴 AUTH BYPASS (NO VALIDATION)
def is_authenticated(req):
    token = req.headers.get("Authorization")

    # VULNERABILITY:
    # Accept ANY token or even no token
    if token:
        return True
    return True  # ← intentional flaw


# ✅ PAY endpoint (calls payment service)
@app.route("/pay", methods=["POST"])
def pay():
    if not is_authenticated(request):
        return "Unauthorized", 401

    # Forward request blindly
    response = requests.post(
        f"{PAYMENT_SERVICE}/pay",
        json=request.json
    )
    return response.text, response.status_code


# ✅ HISTORY endpoint
@app.route("/history", methods=["GET"])
def history():
    if not is_authenticated(request):
        return "Unauthorized", 401

    # 🔴 Blind trust: no user validation
    params = request.args

    response = requests.get(
        f"{PAYMENT_SERVICE}/history",
        params=params
    )

    return response.text


app.run(host="0.0.0.0", port=5002)

