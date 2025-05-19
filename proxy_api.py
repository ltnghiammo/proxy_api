from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import requests

app = Flask(__name__)
CORS(app)

# Đọc key từ biến môi trường, không để trong code!
ABUSEIPDB_KEY = os.environ.get("ABUSEIPDB_KEY", "")
MAXMIND_ID = os.environ.get("MAXMIND_ACCOUNT_ID", "")
MAXMIND_LICENSE = os.environ.get("MAXMIND_LICENSE_KEY", "")
IPQS_API_KEY = os.environ.get("IPQS_API_KEY", "")
IPINFO_TOKEN = os.environ.get("IPINFO_TOKEN", "")

@app.route('/fullcheck')
def fullcheck():
    ip = request.args.get("ip", "")
    result = {"ip": ip}
    # 1. IPInfo
    try:
        geo = requests.get(f"https://ipinfo.io/{ip}/json?token={IPINFO_TOKEN}", timeout=5).json()
        result["geo"] = geo
    except Exception as e:
        result["geo"] = {"error": str(e)}

    # 2. AbuseIPDB
    try:
        headers = {"Accept": "application/json", "Key": ABUSEIPDB_KEY}
        r = requests.get(f"https://api.abuseipdb.com/api/v2/check?ipAddress={ip}&maxAgeInDays=90", headers=headers, timeout=5)
        result["abuse"] = r.json()
    except Exception as e:
        result["abuse"] = {"error": str(e)}

    # 3. MaxMind
    try:
        url = 'https://minfraud.maxmind.com/minfraud/v2.0/score'
        data = {"device": {"ip_address": ip}}
        r = requests.post(url, json=data, auth=(MAXMIND_ID, MAXMIND_LICENSE), timeout=6)
        result["maxmind"] = r.json()
    except Exception as e:
        result["maxmind"] = {"error": str(e)}

    # 4. IPQualityScore
    try:
        r = requests.get(f"https://ipqualityscore.com/api/json/ip/{IPQS_API_KEY}/{ip}", timeout=6)
        result["ipqs"] = r.json()
    except Exception as e:
        result["ipqs"] = {"error": str(e)}

    # 5. RealTest Google
    try:
        google = requests.get("https://www.google.com/search?q=proxy", timeout=6)
        if google.status_code == 200:
            result["realtest"] = "OK"
        else:
            result["realtest"] = f"Blocked ({google.status_code})"
    except Exception as e:
        result["realtest"] = f"Blocked ({e})"

    return jsonify(result)

@app.route('/')
def home():
    return 'API ready!'

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
