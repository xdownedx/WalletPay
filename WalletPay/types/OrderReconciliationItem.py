from typing import Dict
from .WebhookData import MoneyAmount, PaymentOption


class OrderReconciliationItem:
    """
    Represents an item in the order reconciliation list based on the response schema of the API.

    Attributes:
        id (int): Unique identifier for the order.
        status (str): Status of the order, can be one of "ACTIVE", "EXPIRED", "PAID", or "CANCELLED".
        amount (dict): Dictionary representing the order amount. This contains subfields like the actual amount, amountFee, amountNet, and the exchange rate.
        extrenal_id (str): External identifier for the order.
        customer_telegram_user_id (int, optional): Telegram user ID of the order customer.
        created_date_time (str): ISO-8601 date-time indicating when the order was created.
        expiration_date_time (str): ISO-8601 date-time indicating the expiration of the order timeout.
        payment_date_time (str, optional): ISO-8601 date-time indicating when the order was paid.
        selected_payment_option (dict): Represents the payment option selected by the user. This has subfields related to the amount, fees, net amount, and exchange rates.

    Note:
    The attributes are populated based on the 'items' field in the 'data' field of the API response when the status is "SUCCESS".
    """

    def __init__(self, data: Dict):
        """
        Initializes the OrderReconciliationItem object with data from the API response.

        :param data: Dictionary containing details of an order reconciliation item.
        """
        self.id = data["id"]
        self.status = data["status"]
        self.amount = MoneyAmount(data["amount"])
        self.extrenal_id = data["externalId"]
        # The customerTelegramUserId and paymentDateTime fields are optional, they are fetched using the get() method.
        self.customer_telegram_user_id = data.get("customerTelegramUserId")
        self.created_date_time = data["createdDateTime"]
        self.expiration_date_time = data["expirationDateTime"]
        self.payment_date_time = data.get("paymentDateTime")
        self.selected_payment_option = PaymentOption(
            data["selectedPaymentOption"]) if "selectedPaymentOption" in data else None

    def __str__(self) -> str:
        """
        Returns a string representation of the OrderReconciliationItem object, useful for logging or debugging purposes.

        :return: String representation of the OrderReconciliationItem.
        """
        return (f"OrderReconciliationItem(id={self.id}, status={self.status}, "
                f"amount={self.amount.amount, self.amount.currencyCode}, extrenal_id={self.extrenal_id})")
