# app/services/explorium.py
import requests
import os
from pathlib import Path 
from dotenv import load_dotenv
env_path = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(env_path)

EXPLORIUM_API_KEY = os.getenv("EXPLORIUM_API_KEY")
EXPLORIUM_URL = "https://api.explorium.ai/v1/businesses/firmographics/enrich"


def getBID(domain: str) -> str :
    headers = {"Authorization": f"Bearer {EXPLORIUM_API_KEY}"}
    payload = {"domain": domain}

    try:
        res = requests.post("https://api.explorium.ai/v1/businesses/match",json=payload, headers=headers, timeout=10)
        data = res.json()
        print(data.get("busi"))
        return data.get("business_id")
    except Exception as e: 
        raise e

def enrich_company(domain: str) -> dict:
    businessId = getBID(domain)

    headers = {"Authorization": f"Bearer {EXPLORIUM_API_KEY}"}
    payload = {"domain": businessId}

    try:
        response = requests.post(EXPLORIUM_URL, json=payload, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()

        # Map API response to our DB fields
        return {
            "industry": data.get("naics_description"),
            "company_size": data.get("number_of_employees_range"),
            "revenue_range": data.get("yearly_revenue_range"),
        }

    except Exception as e:
        print(f"[Explorium API Error] {e}")
        return {}