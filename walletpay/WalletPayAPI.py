import requests
import json
from . import Order, WalletPayException
class WalletPayAPI:
    BASE_URL = "https://pay.wallet.tg/wpay/store-api/v1/"

    def __init__(self, api_key):
        self.api_key = api_key

    def _make_request(self, method, endpoint, data=None):
        """Internal method to make API requests."""
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

    def create_order(self, amount, currency_code, description, external_id, timeout_seconds, customer_telegram_user_id, return_url=None, fail_return_url=None, custom_data=None):
        """Create a new order."""
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
        return None

    def get_order_preview(self, order_id):
        """Retrieve the order information."""
        response_data = self._make_request("GET", f"order/preview?id={order_id}")
        if response_data.get("status") == "SUCCESS":
            return Order(response_data.get("data"))
        return None

    def get_order_list(self, offset, count):
        """Return list of store orders."""
        response_data = self._make_request("GET", f"reconciliation/order-list?offset={offset}&count={count}")
        if response_data.get("status") == "SUCCESS":
            orders_data = response_data.get("data", {}).get("items", [])
            return [Order(order_data) for order_data in orders_data]
        return []

    def get_order_amount(self):
        """Return Store orders amount."""
        response_data = self._make_request("GET", "reconciliation/order-amount")
        if response_data.get("status") == "SUCCESS":
            return int(response_data.get("data", {}).get("totalAmount", 0))
        return 0