from typing import Dict
from .WebhookData import MoneyAmount


class OrderPreview:
    """
    Represents a preview of an order based on the response schema of a specific API.

    Attributes:
        id (str): The order's unique identifier.
        status (str): Status of the order, can be one of "ACTIVE", "EXPIRED", "PAID", or "CANCELLED".
        number (str): A human-readable short order ID shown to customers.
        amount (dict): A dictionary representing the amount and currency of the order.
        created_date_time (str): ISO-8601 date-time indicating when the order was created.
        expiration_date_time (str): ISO-8601 date-time indicating the expiration of the order timeout.
        completed_date_time (str, optional): ISO-8601 date-time indicating when the order was completed (e.g., paid, expired).
        pay_link (str): URL for payment. Should be shown to the payer by the store in a Telegram Bot context.
            Note: This link can only be opened in the dialog with the specified Telegram bot in the store, and only by the user with the specified telegramUserId in the order.
        direct_pay_link (str): URL for direct payment. Can be used in both 'Telegram Bot' and 'Telegram Web App' contexts.
            Note: As with pay_link, there are restrictions on who can open this link.

    Note:
    The attributes are populated based on the 'data' field of the API response when the status is "SUCCESS".
    """

    def __init__(self, data: Dict):
        """
        Initializes the OrderPreview object with data from the API response.

        :param data: Dictionary containing order preview details.
        """
        self.id = data["id"]
        self.status = data["status"]
        self.number = data["number"]
        self.amount = MoneyAmount(data["amount"])
        self.created_date_time = data["createdDateTime"]
        self.expiration_date_time = data["expirationDateTime"]
        # The completedDateTime field is optional, so it's fetched with the get() method.
        self.completed_date_time = data.get("completedDateTime")
        self.pay_link = data["payLink"]
        self.direct_pay_link = data["directPayLink"]

    def __str__(self) -> str:
        """
        Returns a string representation of the OrderPreview object, which can be useful for logging or debugging.

        :return: String representation of the OrderPreview.
        """
        return (f"OrderPreview(id={self.id}, status={self.status}, number={self.number}, "
                f"amount={self.amount.amount, self.amount.currencyCode})")
