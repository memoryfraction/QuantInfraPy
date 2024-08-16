# Define an interface
from abc import ABC, abstractmethod

from shared_lib.bll.utility import Utility


class IPaymentProcessor(ABC):
    @abstractmethod
    def process_payment(self, amount):
        pass


# Create implementations of the interface
class CreditCardPaymentProcessor(IPaymentProcessor):
    def __init__(self, utility: Utility):
        self.utility = utility

    def process_payment(self, amount):
        return f"Processing credit card payment of ${amount}"


class PayPalPaymentProcessor(IPaymentProcessor):
    def process_payment(self, amount):
        return f"Processing PayPal payment of ${amount}"
