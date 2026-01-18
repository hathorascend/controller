"""Configuration and constants for the payment controller application."""

from typing import TypedDict, List

# ========== Application Settings ==========
YEAR: int = 2026
CONTROL_DAY: int = 29  # Reference control day (month cutoff)

# ========== File Paths ==========
DATA_FOLDER: str = "data"
DATA_FILE: str = "control_pagos_streamlit_2026.json"
LOG_FILE: str = "operaciones.txt"

# ========== Account Definitions ==========
class AccountDict(TypedDict):
    """Type definition for account dictionary."""
    id: int
    name: str

ACCOUNTS: List[AccountDict] = [
    {"id": 1, "name": "BBVA – Ydaliz"},
    {"id": 2, "name": "BBVA – Moisés"},
    {"id": 3, "name": "Caixa – Conjunta"},
    {"id": 4, "name": "Santander – Ydaliz"},
    {"id": 5, "name": "Santander – Moisés"},
]

# Account lookup by ID
ACCOUNT_BY_ID: dict = {acc["id"]: acc["name"] for acc in ACCOUNTS}

# ========== Template: Fixed Expenses ==========
FIXED_EXPENSES: List[dict] = [
    {"id": 1, "name": "Cuota hipoteca", "amount": 533.66, "day": 5, "account_id": 4},
    {"id": 2, "name": "Seguro hogar", "amount": 66.00, "day": 10, "account_id": 4},
    {"id": 3, "name": "Seguro de vida", "amount": 52.00, "day": 10, "account_id": 3},
    {"id": 4, "name": "Crédito coche", "amount": 258.00, "day": 15, "account_id": 1},
    {"id": 5, "name": "Crédito complementario casa", "amount": 385.00, "day": 15, "account_id": 3},
    {"id": 6, "name": "Cofidis", "amount": 145.00, "day": 20, "account_id": 1},
    {"id": 7, "name": "IKEA Yda", "amount": 200.00, "day": 25, "account_id": 1},
    {"id": 8, "name": "IKEA Moisés", "amount": 200.00, "day": 25, "account_id": 5},
    {"id": 9, "name": "Vodafone", "amount": 15.00, "day": 8, "account_id": 1},
    {"id": 10, "name": "Orange", "amount": 240.00, "day": 8, "account_id": 2},
    {"id": 11, "name": "Carrefour", "amount": 100.00, "day": 12, "account_id": 1},
    {"id": 12, "name": "Agua", "amount": 60.00, "day": 18, "account_id": 3},
    {"id": 13, "name": "Luz", "amount": 120.00, "day": 18, "account_id": 3},
    {"id": 14, "name": "Comida", "amount": 800.00, "day": 2, "account_id": 3},
    {"id": 15, "name": "Curso inglés niño", "amount": 80.00, "day": 7, "account_id": 4},
    {"id": 16, "name": "Karate", "amount": 50.00, "day": 7, "account_id": 4},
    {"id": 17, "name": "Gasolina", "amount": 100.00, "day": 1, "account_id": 4},
]

# ========== Template: Monthly Subscriptions ==========
MONTHLY_SUBSCRIPTIONS: List[dict] = [
    {"id": 101, "name": "ChatGPT Plus", "amount": 22.99, "day": 2, "account_id": 2},
    {"id": 102, "name": "Netflix", "amount": 16.00, "day": 2, "account_id": 2},
    {"id": 103, "name": "iCloud+ (2 TB)", "amount": 9.99, "day": 8, "account_id": 2},
    {"id": 104, "name": "PS Plus", "amount": 16.00, "day": 15, "account_id": 2},
    {"id": 105, "name": "Proton VPN Plus", "amount": 12.99, "day": 19, "account_id": 2},
    {"id": 106, "name": "X Premium", "amount": 4.00, "day": 27, "account_id": 2},
    {"id": 107, "name": "Roblox (niño)", "amount": 11.00, "day": 30, "account_id": 2},
]

# ========== Template: Annual Subscriptions ==========
ANNUAL_SUBSCRIPTIONS: List[dict] = [
    {"id": 201, "name": "InShot Pro (Anual)", "amount": 15.99, "day": 8, "account_id": 2, "annual_month": 5},
    {"id": 202, "name": "Telegram Premium (Anual)", "amount": 33.99, "day": 25, "account_id": 2, "annual_month": 9},
]

# ========== Utility Functions ==========
def get_all_template_items() -> List[dict]:
    """Combine all template items (fixed, monthly, annual)."""
    return [
        {**item, "type": "fixed"} for item in FIXED_EXPENSES
    ] + [
        {**item, "type": "sub_monthly"} for item in MONTHLY_SUBSCRIPTIONS
    ] + [
        {**item, "type": "sub_annual"} for item in ANNUAL_SUBSCRIPTIONS
    ]
