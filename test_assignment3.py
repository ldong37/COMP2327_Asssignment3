"""
Unit tests for the Strategy and Observer pattern additions.
"""

__author__ = "Dong Le Quoc Bao"
__version__ = "1.0.0"


from decimal import Decimal
from types import SimpleNamespace
import unittest

from account.account_status import AccountStatus
from account.bank_account import BankAccount
from events.event import Event
from events.logging_listener import LoggingListener
from fee.base_percentage_fee_strategy import BasePercentageFeeStrategy
from fee.percentage_fee_strategy import PercentageFeeStrategy
from transaction.bank_transfer_transaction import BankTransferTransaction
from transaction.credit_card_transaction import CreditCardTransaction


class RecordingListener:
    """A small listener used to verify event notifications."""

    def __init__(self) -> None:
        self.senders = []

    def update(self, sender) -> None:
        self.senders.append(sender)


class Assignment3Tests(unittest.TestCase):
    """Tests for fee strategies, events, and transaction notifications."""

    def make_account(self, account_id: int, balance: str) -> BankAccount:
        owner = SimpleNamespace(name="Test User")
        return BankAccount(
            account_id,
            Decimal(balance),
            owner,
            AccountStatus.ACTIVE,
        )

    def test_percentage_fee_is_rounded_to_two_decimal_places(self) -> None:
        strategy = PercentageFeeStrategy(Decimal("0.0035"))
        self.assertEqual(strategy.get_fee(Decimal("1000.00")), Decimal("3.50"))

    def test_percentage_fee_accepts_zero_and_one(self) -> None:
        self.assertEqual(
            PercentageFeeStrategy(Decimal("0")).get_fee(Decimal("10")),
            Decimal("0.00"),
        )
        self.assertEqual(
            PercentageFeeStrategy(Decimal("1")).get_fee(Decimal("10")),
            Decimal("10.00"),
        )

    def test_percentage_fee_rejects_out_of_range_percentage(self) -> None:
        with self.assertRaisesRegex(
            ValueError,
            "percentage must be a value between 0 and 1 (inclusive)$",
        ):
            PercentageFeeStrategy(Decimal("1.01"))

    def test_base_percentage_fee_uses_greater_fee_and_rounds(self) -> None:
        base_strategy = BasePercentageFeeStrategy(
            Decimal("1.26"), Decimal("0.0007")
        )
        percentage_strategy = BasePercentageFeeStrategy(
            Decimal("1.00"), Decimal("0.02")
        )
        self.assertEqual(
            base_strategy.get_fee(Decimal("1000.00")), Decimal("1.26")
        )
        self.assertEqual(
            percentage_strategy.get_fee(Decimal("100.00")), Decimal("2.00")
        )

    def test_base_fee_rejects_negative_base_fee(self) -> None:
        with self.assertRaisesRegex(
            ValueError,
            "base_fee must be greater than or equal to zero$",
        ):
            BasePercentageFeeStrategy(Decimal("-0.01"), Decimal("0.01"))

    def test_event_add_remove_and_notify(self) -> None:
        event = Event()
        listener = RecordingListener()

        event.notify("no listeners")
        event.add_listener(listener)
        event.notify("first event")
        self.assertEqual(listener.senders, ["first event"])

        event.remove_listener(listener)
        event.remove_listener(listener)  # Removing an absent listener is safe.
        event.notify("after removal")
        self.assertEqual(listener.senders, ["first event"])

    def test_credit_card_transaction_notifies_after_success(self) -> None:
        account = self.make_account(1001, "1000.00")
        transaction = CreditCardTransaction(
            "CC-001", Decimal("100.00"), account, "AUTH-001"
        )
        listener = RecordingListener()
        transaction.on_processed.add_listener(listener)

        transaction.process()

        self.assertEqual(transaction.status.name, "PROCESSED")
        self.assertEqual(account.balance, Decimal("900.00"))
        self.assertEqual(listener.senders, [transaction])

    def test_bank_transfer_without_fee_strategy_succeeds(self) -> None:
        source = self.make_account(1001, "1000.00")
        target = self.make_account(1002, "100.00")
        transaction = BankTransferTransaction(
            "BT-001", Decimal("50.00"), source, target
        )

        transaction.process()

        self.assertEqual(transaction.status.name, "PROCESSED")
        self.assertEqual(source.balance, Decimal("950.00"))
        self.assertEqual(target.balance, Decimal("150.00"))

    def test_logging_listener_rejects_non_transaction_sender(self) -> None:
        with self.assertRaisesRegex(
            TypeError, "sender must be a Transaction type$"
        ):
            LoggingListener().update(object())


if __name__ == "__main__":
    unittest.main()
