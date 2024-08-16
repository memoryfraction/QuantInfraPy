from shared_lib.bll.payment_processor import IPaymentProcessor


class PaymentGateway:
    def __init__(self, payment_processor: IPaymentProcessor):
        self.payment_processor = payment_processor

    def complete_purchase(self, amount):
        payment_result = self.payment_processor.process_payment(amount)
        return f"Payment completed: {payment_result}"