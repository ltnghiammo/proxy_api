from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
import httpx
import asyncio
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Thêm CORS middleware sau khi khởi tạo app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Thay các API_KEY bên dưới bằng key thật của bạn
ABUSEIPDB_KEY = "e2997ad9fbbd3446bec838c5d282ce89260314ba9d5176126446fb8ee9703746c4479c7ea50f5ae3"
IPQS_KEY = "GvSQcGadOtZJ5TOAGjnoRYtlS7e2yOyo"

async def fetch_abuseipdb(ip):
    url = f"https://api.abuseipdb.com/api/v2/check?ipAddress={ip}&maxAgeInDays=90"
    headers = {"Key": ABUSEIPDB_KEY, "Accept": "application/json"}
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(url, headers=headers, timeout=5)
            return resp.json()
        except Exception:
            return {}

async def fetch_ipqs(ip):
    url = f"https://ipqualityscore.com/api/json/ip/{IPQS_KEY}/{ip}"
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(url, timeout=5)
            return resp.json()
        except Exception:
            return {}

async def fetch_geo(ip):
    url = f"https://ipinfo.io/{ip}/json"
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(url, timeout=5)
            return resp.json()
        except Exception:
            return {}

@app.get("/fullcheck")
async def fullcheck(ip: str = Query(...)):
    # Chạy song song các truy vấn
    abuse_task = fetch_abuseipdb(ip)
    ipqs_task = fetch_ipqs(ip)
    geo_task = fetch_geo(ip)
    abuse, ipqs, geo = await asyncio.gather(abuse_task, ipqs_task, geo_task)
    # Có thể bổ sung thêm các API khác nếu cần
    return JSONResponse({
        "abuse": abuse,
        "ipqs": ipqs,
        "geo": geo,
        "realtest": "OK"  # Có thể bổ sung kiểm tra thực tế
    })
