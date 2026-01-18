"""Business logic and calculation engine for payment controller.

This module provides core calculations, validations, and business logic
for the payment control system. All calculations are type-hinted and
include comprehensive error handling.
"""

from typing import Dict, Tuple, List, Optional
from decimal import Decimal
from datetime import datetime
from enum import Enum
from dataclasses import dataclass


class PaymentStatus(str, Enum):
    """Enumeration of possible payment statuses."""
    PENDING = "pending"
    CONFIRMED = "confirmed"
    PROCESSED = "processed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class TransactionType(str, Enum):
    """Types of financial transactions."""
    INCOME = "income"
    EXPENSE = "expense"
    TRANSFER = "transfer"
    ADJUSTMENT = "adjustment"


class TaxMethod(str, Enum):
    """Tax calculation methods."""
    SIMPLE = "simple"
    PROGRESSIVE = "progressive"
    FLAT_RATE = "flat_rate"


@dataclass
class CalculationResult:
    """Result container for calculation operations."""
    value: Decimal
    metadata: Dict[str, any] = None
    is_valid: bool = True
    error_message: Optional[str] = None


class PaymentCalculator:
    """Core calculations for payment processing and analysis."""

    MIN_AMOUNT: Decimal = Decimal("0.01")
    MAX_AMOUNT: Decimal = Decimal("999999.99")
    DEFAULT_TAX_RATE: Decimal = Decimal("0.21")  # 21% VAT

    @staticmethod
    def validate_amount(amount: Decimal) -> Tuple[bool, Optional[str]]:
        """Validate payment amount against constraints."""
        if amount < PaymentCalculator.MIN_AMOUNT:
            return False, f"Amount must be at least {PaymentCalculator.MIN_AMOUNT}"
        if amount > PaymentCalculator.MAX_AMOUNT:
            return False, f"Amount exceeds maximum {PaymentCalculator.MAX_AMOUNT}"
        return True, None

    @staticmethod
    def calculate_tax(base_amount: Decimal, tax_rate: Decimal = None) -> CalculationResult:
        """Calculate tax on a base amount.
        
        Args:
            base_amount: Amount before tax
            tax_rate: Tax rate (default 21%)
            
        Returns:
            CalculationResult with tax calculation details
        """
        if tax_rate is None:
            tax_rate = PaymentCalculator.DEFAULT_TAX_RATE

        is_valid, error = PaymentCalculator.validate_amount(base_amount)
        if not is_valid:
            return CalculationResult(Decimal("0"), is_valid=False, error_message=error)

        tax_amount = (base_amount * tax_rate).quantize(Decimal("0.01"))
        return CalculationResult(
            value=tax_amount,
            metadata={
                "base_amount": str(base_amount),
                "tax_rate": str(tax_rate),
                "total_with_tax": str(base_amount + tax_amount)
            },
            is_valid=True
        )

    @staticmethod
    def calculate_total_with_tax(
        base_amount: Decimal,
        tax_rate: Decimal = None
    ) -> Decimal:
        """Calculate total amount including tax."""
        if tax_rate is None:
            tax_rate = PaymentCalculator.DEFAULT_TAX_RATE
        return (base_amount * (1 + tax_rate)).quantize(Decimal("0.01"))

    @staticmethod
    def calculate_discount(amount: Decimal, discount_percent: Decimal) -> CalculationResult:
        """Calculate discount on an amount."""
        if not (0 <= discount_percent <= 100):
            return CalculationResult(
                Decimal("0"),
                is_valid=False,
                error_message="Discount must be between 0 and 100%"
            )

        discount_amount = (amount * discount_percent / 100).quantize(Decimal("0.01"))
        final_amount = (amount - discount_amount).quantize(Decimal("0.01"))
        
        return CalculationResult(
            value=final_amount,
            metadata={
                "original_amount": str(amount),
                "discount_percent": str(discount_percent),
                "discount_amount": str(discount_amount)
            },
            is_valid=True
        )

    @staticmethod
    def calculate_commission(
        amount: Decimal,
        commission_rate: Decimal
    ) -> CalculationResult:
        """Calculate commission on a transaction."""
        commission = (amount * commission_rate / 100).quantize(Decimal("0.01"))
        net_amount = (amount - commission).quantize(Decimal("0.01"))
        
        return CalculationResult(
            value=net_amount,
            metadata={
                "gross_amount": str(amount),
                "commission_rate": str(commission_rate),
                "commission_amount": str(commission),
                "net_amount": str(net_amount)
            },
            is_valid=True
        )


class BalanceCalculator:
    """Calculations related to balance management."""

    @staticmethod
    def calculate_balance(
        transactions: List[Dict[str, any]]
    ) -> Tuple[Decimal, Decimal, Decimal]:
        """Calculate total balance from transactions.
        
        Returns:
            Tuple of (total_balance, total_income, total_expenses)
        """
        total_income = Decimal("0")
        total_expenses = Decimal("0")

        for transaction in transactions:
            amount = Decimal(str(transaction.get("amount", 0)))
            tx_type = transaction.get("type", TransactionType.EXPENSE)

            if tx_type == TransactionType.INCOME or tx_type == "income":
                total_income += amount
            elif tx_type == TransactionType.EXPENSE or tx_type == "expense":
                total_expenses += amount

        total_balance = (total_income - total_expenses).quantize(Decimal("0.01"))
        return total_balance, total_income, total_expenses

    @staticmethod
    def project_balance(
        current_balance: Decimal,
        monthly_income: Decimal,
        monthly_expenses: Decimal,
        months: int
    ) -> List[Dict[str, Decimal]]:
        """Project balance over specified months."""
        projections = []
        balance = current_balance

        for month in range(1, months + 1):
            balance = (balance + monthly_income - monthly_expenses).quantize(Decimal("0.01"))
            projections.append({
                "month": month,
                "projected_balance": balance,
                "monthly_change": (monthly_income - monthly_expenses).quantize(Decimal("0.01"))
            })

        return projections


class ReportCalculator:
    """Calculations for generating financial reports."""

    @staticmethod
    def calculate_summary(
        transactions: List[Dict[str, any]]
    ) -> Dict[str, any]:
        """Generate comprehensive transaction summary."""
        if not transactions:
            return {
                "total_transactions": 0,
                "total_amount": Decimal("0"),
                "average_amount": Decimal("0"),
                "max_amount": Decimal("0"),
                "min_amount": Decimal("0")
            }

        amounts = [Decimal(str(t.get("amount", 0))) for t in transactions]
        total_amount = sum(amounts).quantize(Decimal("0.01"))
        average_amount = (total_amount / len(transactions)).quantize(Decimal("0.01"))

        return {
            "total_transactions": len(transactions),
            "total_amount": total_amount,
            "average_amount": average_amount,
            "max_amount": max(amounts),
            "min_amount": min(amounts),
            "timestamp": datetime.now().isoformat()
        }
