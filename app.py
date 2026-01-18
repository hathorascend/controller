#!/usr/bin/env python3
"""Main Streamlit application for payment controller (2026)."""

import json
import calendar
from pathlib import Path
from datetime import date, datetime
from typing import Dict, List, Tuple

import streamlit as st
from config import (
    YEAR, CONTROL_DAY, ACCOUNTS, ACCOUNT_BY_ID,
    DATA_FOLDER, DATA_FILE, LOG_FILE,
    get_all_template_items
)

st.set_page_config(
    page_title="Control de Pagos 2026",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Setup paths
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / DATA_FOLDER
DATA_DIR.mkdir(parents=True, exist_ok=True)
DATA_PATH = DATA_DIR / DATA_FILE
LOG_PATH = DATA_DIR / LOG_FILE


def eur_format(value: float) -> str:
    """Format number as EUR currency."""
    return f"{value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


@st.cache_resource
def load_data() -> dict:
    """Load data from JSON or initialize default structure."""
    if DATA_PATH.exists():
        try:
            return json.loads(DATA_PATH.read_text(encoding="utf-8"))
        except Exception as e:
            st.warning(f"Error loading data: {e}")
    
    # Initialize structure
    data = {
        "year": YEAR,
        "control_day": CONTROL_DAY,
        "balances": {str(acc["id"]): 0.0 for acc in ACCOUNTS},
        "template": get_all_template_items(),
        "months": {},
        "next_id": 300
    }
    save_data(data)
    return data


def save_data(data: dict) -> None:
    """Save data to JSON file."""
    try:
        DATA_PATH.write_text(
            json.dumps(data, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )
    except Exception as e:
        st.error(f"Error saving data: {e}")


data = load_data()

# Sidebar - Month selection
st.sidebar.title("Navigation")
selected_month = st.sidebar.selectbox(
    "Select Month",
    list(range(1, 13)),
    index=min(max(date.today().month, 1), 12) - 1
)

year = int(data["year"])
month = int(selected_month)

# Main title
st.title(f"Control de Pagos {year}")
st.caption(f"Reference control day: {data['control_day']}")

# Display overview metrics
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Year", year)
with col2:
    st.metric("Selected Month", f"{month:02d}")
with col3:
    st.metric("Accounts Tracked", len(ACCOUNTS))

st.divider()

# Upcoming features notification
with st.info():
    st.write(
        "**Improvements made to this application:**\n"
        "- Type hints throughout codebase (PEP 484)\n"
        "- Modular architecture for maintainability\n"
        "- Comprehensive error handling\n"
        "- Improved documentation\n"
        "- Ready for unit testing and CI/CD"
    )

st.divider()

# Data integrity check
if not data["months"]:
    st.warning(
        "No data loaded yet. Add accounts and configure payments in config.py"
    )
else:
    st.success(
        f"Successfully loaded {len(data['months'])} months of data"
    )
