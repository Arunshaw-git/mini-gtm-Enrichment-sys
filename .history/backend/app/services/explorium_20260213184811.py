import random
import time


def enrich_company(domain: str) -> dict:
    """
    Simulates an Explorium enrichment API call.
    Replace this with real HTTP request later.
    """

    # simulate network delay
    time.sleep(2)

    # simulate occasional failure
    if random.random() < 0.1:
        raise Exception("Explorium API temporary failure")

    return {
        "industry": random.choice(
            ["SaaS", "Fintech", "E-commerce", "AI", "Healthcare"]
        ),
        "company_size": random.choice(
            ["1-10", "11-50", "51-200", "201-1000", "1000+"]
        ),
        "revenue_range": random.choice(
            ["0-1M", "1M-10M", "10M-100M", "100M+"]
        ),
    }