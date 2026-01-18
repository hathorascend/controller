"""Unit tests for payment calculator module.

This module contains comprehensive tests for all calculator functions
including tax calculations, discounts, commissions, and balance operations.
"""

import pytest
from decimal import Decimal
from calculators import (
    PaymentCalculator,
    BalanceCalculator,
    ReportCalculator,
    CalculationResult
)


class TestPaymentCalculator:
    """Test suite for PaymentCalculator class."""

    def test_validate_amount_valid(self) -> None:
        """Test validation of valid payment amounts."""
        is_valid, error = PaymentCalculator.validate_amount(Decimal("100.00"))
        assert is_valid is True
        assert error is None

    def test_validate_amount_too_small(self) -> None:
        """Test validation rejects amounts below minimum."""
        is_valid, error = PaymentCalculator.validate_amount(Decimal("0.001"))
        assert is_valid is False
        assert error is not None

    def test_validate_amount_too_large(self) -> None:
        """Test validation rejects amounts above maximum."""
        is_valid, error = PaymentCalculator.validate_amount(Decimal("1000000.00"))
        assert is_valid is False
        assert error is not None

    def test_calculate_tax_default_rate(self) -> None:
        """Test tax calculation with default rate (21%)."""
        result = PaymentCalculator.calculate_tax(Decimal("100.00"))
        assert result.is_valid is True
        assert result.value == Decimal("21.00")
        assert result.metadata["tax_rate"] == "0.21"

    def test_calculate_tax_custom_rate(self) -> None:
        """Test tax calculation with custom rate."""
        result = PaymentCalculator.calculate_tax(
            Decimal("100.00"),
            Decimal("0.10")
        )
        assert result.is_valid is True
        assert result.value == Decimal("10.00")

    def test_calculate_tax_invalid_amount(self) -> None:
        """Test tax calculation rejects invalid amounts."""
        result = PaymentCalculator.calculate_tax(Decimal("-50.00"))
        assert result.is_valid is False

    def test_calculate_total_with_tax(self) -> None:
        """Test total amount calculation including tax."""
        total = PaymentCalculator.calculate_total_with_tax(
            Decimal("100.00"),
            Decimal("0.21")
        )
        assert total == Decimal("121.00")

    def test_calculate_discount_valid(self) -> None:
        """Test discount calculation with valid parameters."""
        result = PaymentCalculator.calculate_discount(
            Decimal("100.00"),
            Decimal("10.00")
        )
        assert result.is_valid is True
        assert result.value == Decimal("90.00")
        assert result.metadata["discount_amount"] == "10.00"

    def test_calculate_discount_invalid_percentage(self) -> None:
        """Test discount calculation rejects invalid percentages."""
        result = PaymentCalculator.calculate_discount(
            Decimal("100.00"),
            Decimal("150.00")
        )
        assert result.is_valid is False

    def test_calculate_commission(self) -> None:
        """Test commission calculation."""
        result = PaymentCalculator.calculate_commission(
            Decimal("100.00"),
            Decimal("5.00")
        )
        assert result.is_valid is True
        assert result.value == Decimal("95.00")
        assert result.metadata["commission_amount"] == "5.00"


class TestBalanceCalculator:
    """Test suite for BalanceCalculator class."""

    def test_calculate_balance_empty(self) -> None:
        """Test balance calculation with no transactions."""
        balance, income, expenses = BalanceCalculator.calculate_balance([])
        assert balance == Decimal("0")
        assert income == Decimal("0")
        assert expenses == Decimal("0")

    def test_calculate_balance_with_transactions(self) -> None:
        """Test balance calculation with multiple transactions."""
        transactions = [
            {"amount": 1000, "type": "income"},
            {"amount": 300, "type": "expense"},
            {"amount": 200, "type": "expense"}
        ]
        balance, income, expenses = BalanceCalculator.calculate_balance(transactions)
        assert balance == Decimal("500.00")
        assert income == Decimal("1000.00")
        assert expenses == Decimal("500.00")

    def test_project_balance(self) -> None:
        """Test balance projection over months."""
        projections = BalanceCalculator.project_balance(
            Decimal("1000.00"),
            Decimal("500.00"),
            Decimal("200.00"),
            months=3
        )
        assert len(projections) == 3
        assert projections[0]["month"] == 1
        assert projections[0]["projected_balance"] == Decimal("1300.00")
        assert projections[2]["projected_balance"] == Decimal("1900.00")


class TestReportCalculator:
    """Test suite for ReportCalculator class."""

    def test_calculate_summary_empty(self) -> None:
        """Test summary calculation with no transactions."""
        summary = ReportCalculator.calculate_summary([])
        assert summary["total_transactions"] == 0
        assert summary["total_amount"] == Decimal("0")

    def test_calculate_summary_with_transactions(self) -> None:
        """Test summary calculation with transactions."""
        transactions = [
            {"amount": 100},
            {"amount": 200},
            {"amount": 300}
        ]
        summary = ReportCalculator.calculate_summary(transactions)
        assert summary["total_transactions"] == 3
        assert summary["total_amount"] == Decimal("600.00")
        assert summary["average_amount"] == Decimal("200.00")
        assert summary["max_amount"] == Decimal("300")
        assert summary["min_amount"] == Decimal("100")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
