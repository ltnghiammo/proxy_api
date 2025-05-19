from flask import Flask, request, jsonify
import requests
import os
from flask_cors import CORS     # <-- Thêm dòng này

app = Flask(__name__)
CORS(app)                      # <-- Thêm dòng này

@app.route('/abuseipdb')
def abuseipdb():
    ip = request.args.get('ip')
    API_KEY = os.environ.get("ABUSEIPDB_KEY", "e2997ad9fbbd3446bec838c5d282ce89260314ba9d5176126446fb8ee9703746c4479c7ea50f5ae3")
    url = f"https://api.abuseipdb.com/api/v2/check?ipAddress={ip}&maxAgeInDays=90"
    headers = {"Accept": "application/json", "Key": API_KEY}
    resp = requests.get(url, headers=headers, timeout=5)
    return jsonify(resp.json())

@app.route('/maxmind')
def maxmind():
    ip = request.args.get('ip')
    ACCOUNT_ID = os.environ.get("MAXMIND_ACCOUNT_ID", "1170962")
    LICENSE_KEY = os.environ.get("MAXMIND_LICENSE_KEY", "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")
    url = 'https://minfraud.maxmind.com/minfraud/v2.0/score'
    headers = {'Content-Type': 'application/json'}
    data = {"device": {"ip_address": ip}}
    resp = requests.post(url, json=data, auth=(ACCOUNT_ID, LICENSE_KEY), timeout=5)
    return jsonify(resp.json())

@app.route('/')
def home():
    return 'API ready!'

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
