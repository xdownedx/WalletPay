from typing import Dict


class Event:
    """
    Represents the structure of an event based on the response schema of the API.

    Attributes:
        event_id (str): Unique identifier for the event.
        eventDateTime (str): ISO 8601 timestamp indicating the time of the event, in UTC.
        type (str): Type of the event, e.g., "ORDER_PAID", "ORDER_FAILED".
        payload (Payload): Contains detailed information about the event, such as order details, payment options, etc.

    :param data: A dictionary containing the event data.
    """
    def __init__(self, data: Dict):
        self.event_id = data["eventId"]
        self.eventDateTime = data["eventDateTime"]
        self.type = data["type"]
        self.payload = Payload(payload=data["payload"])


class Payload:
    """
    Represents the payload data of a webhook message based on the response schema of the API.

    Attributes:
        order_id (int): Order ID. Unique identifier for the order.
        order_number (str): Human-readable short order ID shown to the customer.
        external_id (str): Order ID in the Merchant system. Used to prevent order duplications due to request retries.
        status (Optional[str]): Order status. Can be one of "ACTIVE", "EXPIRED", "PAID", "CANCELLED". This field is absent for paid orders.
        custom_data (Optional[str]): Any custom string. Will be provided through webhook and order status polling.
        order_amount (MoneyAmount): Represents details about the order's amount.
        selected_payment_option (Optional[PaymentOption]): Represents the user-selected payment option. This field is absent for failed orders.
        order_completed_datetime (str): ISO 8601 timestamp indicating the time of order completion, in UTC.
    """

    def __init__(self, payload: Dict):
        self.order_id = payload["id"]
        self.order_number = payload["number"]
        self.external_id = payload["externalId"]
        self.status = payload.get("status")
        self.custom_data = payload.get("customData")
        self.order_amount = MoneyAmount(payload["orderAmount"])
        self.selected_payment_option = PaymentOption(
            payload["selectedPaymentOption"]) if "selectedPaymentOption" in payload else None
        self.order_completed_datetime = payload["orderCompletedDateTime"]


class MoneyAmount:
    """
    Represents the structure of amount-related fields based on the response schema of the API.

    :Attributes:
        currencyCode (str): Currency code, can be one of "TON", "BTC", "USDT", "EUR", "USD", "RUB".
        amount (str): Big decimal string representation of the amount.
    """

    def __init__(self, data: Dict):
        self.currencyCode = data["currencyCode"]
        self.amount = data["amount"]


class PaymentOption:
    """
    Represents the payment option selected by the user based on the response schema of the API.

    Attributes:
        amount (MoneyAmount): The order amount details.
        amountFee (MoneyAmount): The fee associated with the order.
        amountNet (MoneyAmount): The net amount after considering the fee.
        exchangeRate (str): Exchange rate of order currency to payment currency.
    """

    def __init__(self, data: Dict):
        self.amount = MoneyAmount(data["amount"])
        self.amountFee = MoneyAmount(data["amountFee"])
        self.amountNet = MoneyAmount(data["amountNet"])
        self.exchangeRate = data["exchangeRate"]
