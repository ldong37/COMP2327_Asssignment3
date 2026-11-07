"""
Common interface for fee strategies.
"""

__author__ = "Dong Le Quoc Bao"
__version__ = "1.0.0"

from abc import ABC, abstractmethod
from decimal import Decimal

class FeeStrategy(ABC):
    """
    Abstract base class for fee strategies.
    This class defines how a transaction fee is calculated.
    """

    @abstractmethod
    def get_fee(self, transaction_amount: Decimal) -> Decimal:
        """
        Return the fee to charge for a transaction.

        Args:
            transaction_amount (Decimal): The amount of money in the transaction.
            
        Returns:
            Decimal: The calculated transaction fee
        """
        raise NotImplementedError
    