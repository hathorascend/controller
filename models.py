"""Data models and type definitions for payment controller."""

from typing import TypedDict, List, Optional, Dict, Any
from datetime import date
from enum import Enum


class PaymentType(str, Enum):
    """Enumeration of payment types."""
    FIXED = "fixed"
    MONTHLY_SUB = "sub_monthly"
    ANNUAL_SUB = "sub_annual"


class Account(TypedDict):
    """Bank account definition."""
    id: int
    name: str


class Expense(TypedDict):
    """Template expense definition."""
    id: int
    name: str
    amount: float
    day: int
    account_id: int
    type: PaymentType
    annual_month: Optional[int]


class MonthlyItem(TypedDict):
    """Monthly payment item."""
    tid: int
    name: str
    amount: float
    account_id: int
    due: str
    paid: bool
    type: PaymentType


class MonthData(TypedDict):
    """Monthly payment data."""
    year: int
    month: int
    items: List[MonthlyItem]


class AppData(TypedDict):
    """Application data structure."""
    year: int
    control_day: int
    balances: Dict[str, float]
    template: List[Dict[str, Any]]
    months: Dict[str, MonthData]
    next_id: int


class ValidationError(Exception):
    """Custom validation error."""
    pass


class StorageError(Exception):
    """Custom storage error."""
    pass
