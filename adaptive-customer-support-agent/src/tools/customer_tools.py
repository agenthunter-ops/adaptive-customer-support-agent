"""
Customer profile stub. In real deployments this wraps your CRM / core.
"""
import random

CUSTOMERS = {
    "alice@example.com": {"name": "Alice", "vip": True},
    "bob@example.com": {"name": "Bob", "vip": False},
}


def get_customer_profile(email: str) -> dict | None:
    profile = CUSTOMERS.get(email)
    if profile:
        profile["loyalty_score"] = random.randint(50, 100)
    return profile
