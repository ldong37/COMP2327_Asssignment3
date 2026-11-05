"""
Fee strategy where the fee is a percentage of the transaction amount.
"""
__author__ = "Dong Le Quoc Bao"
__version__ = "1.0.0"

from decimal import Decimal
from fee.fee_strategy import FeeStrategy

class PercentageFeeStrategy(FeeStrategy):
    """Fee strategy where the fee is a percentage of the transaction amount."""
    
    def __init__(self, percentage: Decimal) -> None:
        """
        Initialize a PercentageFeeStrategy.

        Args:
            percentage (Decimal): The fee percentage (between 0 and 1 exclusive).
        """
        if not (Decimal("0") <= percentage <= Decimal("1")):
            raise ValueError("Percentage must be between 0 and 1 (inclusive).")
        
        self._percentage: Decimal = percentage

    @property
    def percentage(self) -> Decimal:
        """Decimal: The percentage used to calculate the fee"""
        return self._percentage
    
    def get_fee (self,transaction_amount:Decimal) -> Decimal:
        """
        Return the percentage of the transaction amount.
        
        Args:
            transaction_amount (Decimal): The amount of the transaction.
            
        Returns:
            Decimal: The fee, rounded to two decimal places.
        """
        fee = transaction_amount * self._percentage
        return transaction_amount * self._percentage