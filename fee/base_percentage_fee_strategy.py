"""
Fee strategy where the fee is the higher of a base fee and a percentage.
"""

__author__ = "Dong Le Quoc Bao"
__version__ = "1.0.0"

from decimal import Decimal, ROUND_HALF_UP
from fee.percentage_fee_strategy import PercentageFeeStrategy

class BasePercentageFeeStrategy(PercentageFeeStrategy):
    """Fee strategy where the fee is greater of a base fee or a percentage"""
    
    def __init__(self, base_fee: Decimal, percentage: Decimal) -> None:
        """
        Initialize a BasePercentageFeeStrategy.

        Args:
            base_fee (Decimal): The base fee amount.
            percentage (Decimal): The fee percentage (between 0 and 1 inclusive).
        """
        if base_fee < Decimal("0"):
            raise ValueError("Base fee must be greater than or equal to 0")
        super().__init__(percentage)
        self._base_fee: Decimal = base_fee

    @property
    def base_fee(self) -> Decimal:
        """Decimal: The minimum fee applied."""
        return self._base_fee
    
    def get_fee(self, transaction_amount: Decimal) -> Decimal:
        """
        Return the greater of the base fee or the percentage fee.
        
        Args:
            transaction_amount (Decimal): The amount of the transaction.
            
        Returns:
            Decimal: The fee, rounded to two decimal places.
        """
        
        percentage_fee = transaction_amount * self.percentage
        fee = max(self._base_fee, percentage_fee)
        return fee.quantize(Decimal("0.01"), rounding = "ROUND_HALF_UP")