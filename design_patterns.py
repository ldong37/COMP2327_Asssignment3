"""This module includes a program to demonstrate your understanding of
the Design Patterns used in this project.
"""

__author__ = "Dong Le Quoc Bao"
__version__ = "1.0.0"

from decimal import Decimal

from account.account_status import AccountStatus
from account.bank_account import BankAccount
from account.client import Client
from transaction.credit_card_transaction import CreditCardTransaction
from fee.base_percentage_fee_strategy import BasePercentageFeeStrategy
from fee.percentage_fee_strategy import PercentageFeeStrategy
from events.logging_listener import LoggingListener


def main() -> None:
    """The program's main entry point."""
    #set up the client and bank account
    client = Client(1,"John Doe", "johndoe@gmail.com")
    account = BankAccount(777777777, Decimal("5000.00"), client, AccountStatus.ACTIVE)

    # 1. Create a transaction instance.
    transaction = CreditCardTransaction("TXN-001", Decimal("1000.00"), account, "AUTH-12345")

    # 2. Print the transaction fee
    print (f"Fee (no startegy ): {transaction.fees}")
    # 3. Create a new instance of a fee strategy, the transaction fee
    #    is determined by base or percentage, depending which is higher.
    #    The base fee is $1.26 and the percentage of the transaction 
    #    amount is .07%.
    base_pct_strategy = BasePercentageFeeStrategy(Decimal("1.26"), Decimal("0.0007"))
    
    # 4. Update the transaction instance such that it will use the fee
    #    strategy to calculate the fees.
    transaction.set_fee_strategy(base_pct_strategy)
    # 5. Print the transaction fees. Formatting is not required.
    print(f"Fee (base/percentage): {transaction.fees}")
    # 6. Update the transaction instance such that the fee strategy will
    #    determine the fee based only on percentage of the transaction
    #    amount. The fee is .35% of the transaction amount.
    transaction.set_fee_strategy(PercentageFeeStrategy(Decimal("0.0035")))

    # 7. Print the transaction fees. Formatting is not required.
    print(f"Fee (percentage only): {transaction.fees}")

    # 8. Create a logging listener instance.
    listener = LoggingListener()
    # 9. Using the listener, subscribe to the event.
    transaction.on_processed.add_listener(listener)

    # 10. Invoke the method to raise the event.
    transaction.process()

if __name__ == "__main__":
    main()
