# app/services/explorium.py
import requests
import os
from pathlib import Path 
from dotenv import load_dotenv
env_path = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(env_path)

EXPLORIUM_API_KEY = os.getenv("EXPLORIUM_API_KEY")
EXPLORIUM_URL = "https://app.explorium.ai/api/bundle/v1/enrich/firmographics"
def enrich_company(domain: str) -> dict:
    
    print("Loading .env from:", env_path)
    print("explorium called ")
    print(EXPLORIUM_API_KEY)
    headers = {"Authorization": f"Bearer {EXPLORIUM_API_KEY}"}
    payload = {"domain": domain}

    try:
        response = requests.post(EXPLORIUM_URL, json=payload, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()

        # Map API response to our DB fields
        return {
            "industry": data.get("NAICS description"),
            "company_size": data.get("Number of employees range all sites"),
            "revenue_range": data.get("Yearly revenue range range all sites"),
        }

    except Exception as e:
        print(f"[Explorium API Error] {e}")
        return {}