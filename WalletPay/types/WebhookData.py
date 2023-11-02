import datetime
import json
from typing import Any, Dict, Optional, Union


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
        self.event_id: str = data["eventId"]

        # The line of code `self.eventDateTime: datetime.datetime =
        # datetime.datetime.fromisoformat(data["eventDateTime"])` is initializing the `eventDateTime`
        # attribute of the `Event` class.
        self.eventDateTime: datetime.datetime = datetime.datetime.fromisoformat(
            data["eventDateTime"]
        )

        self.type: str = data["type"]
        self.payload: Payload = Payload(payload=data["payload"])


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
        self.order_id: int = payload["id"]
        self.order_number: int = payload["number"]
        self.external_id: str = payload["externalId"]
        self.status: str = payload.get("status")

        # The line of code `self.custom_data: Union[str, Dict[str, Any]] =
        # self.__parse_custom_data(custom_data=payload.get("custom_data"))` is initializing the `custom_data`
        # attribute of the `Payload` class.
        self.custom_data: Union[str, Dict[str, Any]] = self.__parse_custom_data(
            custom_data=payload.get("custom_data")
        )
        self.order_amount: MoneyAmount = MoneyAmount(payload["orderAmount"])

        # The line of code `self.selected_payment_option: Optional[PaymentOption] =
        # (PaymentOption(payload["selectedPaymentOption"]) if "selectedPaymentOption" in payload else
        # None)` is initializing the `selected_payment_option` attribute of the `Payload` class.
        self.selected_payment_option: Optional[PaymentOption] = (
            PaymentOption(payload["selectedPaymentOption"])
            if "selectedPaymentOption" in payload
            else None
        )
        self.completed_date_time: Optional[datetime.datetime] = None

        # The code `if iso_completed_date_time := payload["completedDateTime"]:` is using the walrus
        # operator `:=` to assign the value of `payload["completedDateTime"]` to the variable
        # `iso_completed_date_time` and also checks if the value is truthy (not None or empty).
        if iso_completed_date_time := payload["completedDateTime"]:
            self.completed_date_time: datetime.datetime = (
                datetime.datetime.fromisoformat(iso_completed_date_time)
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
        self.amount: MoneyAmount = MoneyAmount(data["amount"])
        self.amountFee: MoneyAmount = MoneyAmount(data["amountFee"])
        self.amountNet: MoneyAmount = MoneyAmount(data["amountNet"])
        self.exchangeRate: str = data["exchangeRate"]
