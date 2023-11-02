import datetime
import json
from optparse import Option
from typing import Dict, Optional, Union


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
        self.eventDateTime: datetime.datetime = datetime.datetime.fromisoformat(
            data["eventDateTime"]
        )
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

    def __parse_custom_data(
        self, custom_data: Optional[str]
    ) -> Optional[Union[Dict, str]]:
        """
        The function `__parse_custom_data` takes in a string `custom_data` and tries to parse it as JSON,
        returning the parsed JSON if successful, or the original string if parsing fails.

        :param custom_data: The `custom_data` parameter is a string that represents custom data. It is an
        optional parameter, meaning it can be `None` or a string value
        :type custom_data: Optional[str]
        :return: either a dictionary or a string. If the `custom_data` parameter is not empty, it tries to
        parse it as JSON using `json.loads()`. If the parsing is successful, it returns the parsed
        dictionary. If there is a JSONDecodeError, it returns the original `custom_data` as a string. If
        `custom_data` is empty, it returns `None`.
        """
        if custom_data:
            try:
                return json.loads(custom_data)
            except json.JSONDecodeError:
                return custom_data

        return None

    def __init__(self, payload: Dict):
        self.order_id = payload["id"]
        self.order_number = payload["number"]
        self.external_id = payload["externalId"]
        self.status = payload.get("status")
        self.custom_data = self.__parse_custom_data(
            custom_data=payload.get("custom_data")
        )
        self.order_amount = MoneyAmount(payload["orderAmount"])
        self.selected_payment_option = (
            PaymentOption(payload["selectedPaymentOption"])
            if "selectedPaymentOption" in payload
            else None
        )
        self.completed_date_time = payload["completedDateTime"]
        if self.completed_date_time:
            self.completed_date_time: datetime.datetime = (
                datetime.datetime.fromisoformat(self.completed_date_time)
            )


class MoneyAmount:
    """
    Represents the structure of amount-related fields based on the response schema of the API.

    :Attributes:
        currencyCode (str): Currency code, can be one of "TON", "BTC", "USDT", "EUR", "USD", "RUB".
        amount (str): Big decimal string representation of the amount.
    """

    def __init__(self, data: Dict):
        self.currencyCode: str = data["currencyCode"]
        self.amount: int = data["amount"]


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
