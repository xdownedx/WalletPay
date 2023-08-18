# WalletPay API Client

A Python client for interacting with the [WalletPay](https://docs.wallet.tg/pay/#tag/Order-Reconciliation/operation/getOrderAmount) API.

## Installation

Install the package using pip:

```pip install WalletPay```


## Usage
### Synchronous Client

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

# Check if the order is paid
if order_preview.status == "PAID":
    print("Order has been paid!")
else:
    print("Order is not paid yet.")

# Get order list
orders = api.get_order_list(offset=0, count=10)

# Get order amount
amount = api.get_order_amount()

```
### Synchronous Client
To work with the asynchronous client, you'll need an async environment, such as `asyncio`.

```python
import asyncio
from WalletPay import AsyncWalletPayAPI

async def main():
    # Initialize the async API client
    api = AsyncWalletPayAPI(api_key="YOUR_API_KEY")

    # Create an order
    order = await api.create_order(
        amount=100,
        currency_code="USD",
        description="Test Order",
        external_id="12345",
        timeout_seconds=3600,
        customer_telegram_user_id="telegram_user_id"
    )

    # Get order preview
    order_preview = await api.get_order_preview(order_id="ORDER_ID")
    
    # Check if the order is paid
    if order_preview.status == "PAID":
        print("Order has been paid!")
    else:
        print("Order is not paid yet.")
    
    # Get order list
    orders = await api.get_order_list(offset=0, count=10)

    # Get order amount
    amount = await api.get_order_amount()

# Run the async function
asyncio.run(main())

```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Contact

For any questions or feedback, please reach out to [@xdownedx](https://t.me/xdownedx) on Telegram.