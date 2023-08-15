import requests
import json
from typing import Optional, Dict, List
from .Exception import WalletPayException
from .Order import Order

class WalletPayAPI:
    BASE_URL = "https://pay.wallet.tg/wpay/store-api/v1/"

    def __init__(self, api_key: str):
        """
        Initialize the API client.

        :param api_key: The API key to access WalletPay.
        """
        self.api_key = api_key

    def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Dict:
        """
        Internal method to perform API requests.

        :param method: HTTP method ("POST" or "GET").
        :param endpoint: API endpoint.
        :param data: Data to send in the request body (for POST requests).
        :return: Response from the API as a dictionary.

        Source: https://docs.wallet.tg/pay/#api
        """
        headers = {
            'Wpay-Store-Api-Key': self.api_key,
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        url = self.BASE_URL + endpoint

        try:
            if method == "POST":
                response = requests.post(url, headers=headers, data=json.dumps(data))
            elif method == "GET":
                response = requests.get(url, headers=headers)
            else:
                raise WalletPayException("Invalid HTTP method")

            response_data = response.json()

            if response.status_code != 200:
                raise WalletPayException(response_data.get("message", "Unknown error"))

            return response_data

        except requests.RequestException as e:
            raise WalletPayException(f"API request failed: {e}")

    def create_order(self, amount: float, currency_code: str, description: str, external_id: str,
                     timeout_seconds: int, customer_telegram_user_id: str,
                     return_url: Optional[str] = None, fail_return_url: Optional[str] = None,
                     custom_data: Optional[Dict] = None) -> Order:
        """
        Create a new order.

        :param amount: Order amount.
        :param currency_code: Currency code (e.g., "USD").
        :param description: Order description.
        :param external_id: External ID of the order.
        :param timeout_seconds: Payment waiting time in seconds.
        :param customer_telegram_user_id: Telegram user ID.
        :param return_url: URL for redirection after successful payment.
        :param fail_return_url: URL for redirection after failed payment.
        :param custom_data: Additional order data.

        :return: Order object with information about the created order.

        Source: https://docs.wallet.tg/pay/#create-order
        """
        data = {
            "amount": {
                "currencyCode": currency_code,
                "amount": amount
            },
            "description": description,
            "externalId": external_id,
            "timeoutSeconds": timeout_seconds,
            "customerTelegramUserId": customer_telegram_user_id
        }
        if return_url:
            data["returnUrl"] = return_url
        if fail_return_url:
            data["failReturnUrl"] = fail_return_url
        if custom_data:
            data["customData"] = custom_data

        response_data = self._make_request("POST", "order", data)
        if response_data.get("status") == "SUCCESS":
            return Order(response_data.get("data"))
        raise WalletPayException("Failed to create order")

    def get_order_preview(self, order_id: str) -> Order:
        """
        Retrieve order information.

        :param order_id: Order ID.
        :return: Order object with information about the order.

        Source: https://docs.wallet.tg/pay/#get-order-preview
        """
        response_data = self._make_request("GET", f"order/preview?id={order_id}")
        if response_data.get("status") == "SUCCESS":
            return Order(response_data.get("data"))
        raise WalletPayException("Failed to retrieve order preview")

    def get_order_list(self, offset: int, count: int) -> List[Order]:
        """
        Retrieve a list of orders.

        :param offset: Pagination offset.
        :param count: Number of orders to return.
        :return: List of Order objects.

        Source: https://docs.wallet.tg/pay/#get-order-list
        """
        response_data = self._make_request("GET", f"reconciliation/order-list?offset={offset}&count={count}")
        if response_data.get("status") == "SUCCESS":
            orders_data = response_data.get("data", {}).get("items", [])
            return [Order(order_data) for order_data in orders_data]
        raise WalletPayException("Failed to retrieve order list")

    def get_order_amount(self) -> int:
        """
        Retrieve the total amount of all orders.

        :return: Total order amount.

        Source: https://docs.wallet.tg/pay/#get-order-amount
        """
        response_data = self._make_request("GET", "reconciliation/order-amount")
        if response_data.get("status") == "SUCCESS":
            return int(response_data.get("data", {}).get("totalAmount"))
        raise WalletPayException("Failed to retrieve order amount")
