# app/services/explorium.py
import requests
import os

EXPLORIUM_API_KEY = os.getenv("EXPLORIUM_API_KEY")
EXPLORIUM_URL = "https://app.explorium.ai/api/bundle/v1/enrich/firmographics"
def enrich_company(domain: "tesla.com") -> dict:
    """
    Calls Explorium API to enrich company data.
    Returns a dictionary with keys: industry, company_size, revenue_range, etc.
    """
    headers = {"Authorization": f"Bearer {EXPLORIUM_API_KEY}"}
    payload = {"domain": domain}

    try:
        response = requests.post(EXPLORIUM_URL, json=payload, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()

        # Map API response to our DB fields
        data = {
            "industry": data.get("NAICS description"),
            "company_size": data.get("Number of employees range all sites"),
            "revenue_range": data.get("Yearly revenue range range all sites"),
        }
        print(data) 
        print

    except Exception as e:
        print(f"[Explorium API Error] {e}")
        return {}