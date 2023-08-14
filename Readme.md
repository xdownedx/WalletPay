# WalletPay API Client

A Python client for interacting with the WalletPay API.

## Installation

Install the package using pip:

```pip install WalletPay```


## Usage

```python
from WalletPay import WalletPayAPI

# Initialize the API client
api = WalletPayAPI(api_key="YOUR_API_KEY")

# Create an order
order = api.create_order(
    amount=100,
    currency_code="USD",
    description="Test Order",
    external_id="12345",
    timeout_seconds=3600,
    customer_telegram_user_id="telegram_user_id"
)

# Get order preview
order_preview = api.get_order_preview(order_id="ORDER_ID")

# Get order list
orders = api.get_order_list(offset=0, count=10)

# Get order amount
amount = api.get_order_amount()

```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.