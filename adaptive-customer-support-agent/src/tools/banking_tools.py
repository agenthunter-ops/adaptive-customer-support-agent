"""
Placeholder banking back-end integration.
Normally this would call real services for balances, transactions, etc.
Each function returns dummy data to keep the demo safe & self-contained.
"""
from datetime import datetime, timedelta
import random

def get_account_balance(account_id: str) -> dict:
    balance = round(random.uniform(1000, 5000), 2)
    return {
        "account_id": account_id,
        "balance": balance,
        "currency": "USD",
        "as_of": datetime.utcnow().isoformat(),
    }


def get_recent_transactions(account_id: str, days: int = 30) -> list[dict]:
    base_date = datetime.utcnow()
    txns: list[dict] = []
    for _ in range(random.randint(3, 10)):
        delta = timedelta(days=random.randint(1, days))
        txns.append(
            {
                "date": (base_date - delta).strftime("%Y-%m-%d"),
                "amount": round(random.uniform(-200, 200), 2),
                "description": random.choice(
                    ["Restaurant", "ATM Withdrawal", "Salary", "Utility Bill"]
                ),
            }
        )
    return sorted(txns, key=lambda x: x["date"], reverse=True)
