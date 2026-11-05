"""Event listener that logs processed transactions to the console."""

__author__ = "Dong Le Quoc Bao"
__version__ = "1.0.0"

from transaction.transaction import Transaction
from transaction.credit_card_transaction import CreditCardTransaction
from events.event_listener import EventListener

class LoggingListener(EventListener):
    """EventListener that logs transaction processing details to the console"""
    
    def update(self, sender) -> None:
        """
        Log the details of a processed transaction to the console.
        
        Args:
            sender: The object that raised the event.
            
        Raises:
            TypeError: If the sender is not a Transaction.
        """
        
        if not isinstance(sender, Transaction):
            raise TypeError("Sender must be a Transaction type.")
        
        print("TRANSACTION PROCESSED:")
        print(f"ID: {sender.transaction_id}")
        print(f"Status: {sender.status.name}")
        print(f"Amount: {Transaction._format_currency(sender.amount)}")
        print(f"SOURCE ACCOUNT: {sender.account.account_id}")
        
        if isinstance(sender, CreditCardTransaction):
            print(f"AUTH CODE: {sender.authorization_code}")
        
        
        