![MIT License](https://img.shields.io/pypi/l/aiogram.svg?style=flat-square)
![PyPi Package Version](https://img.shields.io/pypi/v/walletpay.svg?style=flat-square)
![Downloads](https://img.shields.io/pypi/dm/walletpay.svg?style=flat-square)
![Supported python versions](https://img.shields.io/pypi/pyversions/walletpay.svg?style=flat-square)

# **WalletPay** API Client

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
### Asynchronous Client
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

## Webhook Integration with Aiogram

To integrate WalletPay webhooks with an Aiogram bot, you can use the `WebhookManager` class. Here's a basic example:

```python
from aiogram import Bot, Dispatcher, types
from WalletPay import WalletPayAPI, WebhookManager
from WalletPay.types import Event
import asyncio

API_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Initialize WalletPay API and WebhookManager
wallet_api = WalletPayAPI(api_key="YOUR_WALLET_API_KEY")
wm = WebhookManager(client=wallet_api)

@wm.successful_handler()
async def handle_successful_event(event: Event):
    # Handle successful payment event
    user_id = "USER_ID"
    await bot.send_message(chat_id=user_id, text=f"Your payment for order {event.payload.order_id}  was successful!")

@wm.failed_handler()
async def handle_failed_event(event: Event):
    # Handle failed payment event
    user_id = "USER_ID"
    await bot.send_message(chat_id=user_id, text=f"Your payment for order {event.payload.order_id} failed. Please try again.")

async def on_startup(dp):
    await bot.send_message(chat_id="YOUR_ADMIN_ID", text="Bot has started!")
    # Start the webhook manager in the background
    asyncio.create_task(wm.start())

async def on_shutdown(dp):
    await bot.send_message(chat_id="YOUR_ADMIN_ID", text="Bot is shutting down!")

# Aiogram bot handlers
@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Welcome to our bot!")

# Start the Aiogram bot
if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)
```
This example demonstrates how to integrate WalletPay webhooks with an Aiogram bot using asyncio and on_startup. When a payment event occurs, the bot will send a message to the user notifying them of the payment status.

#### Note: Ensure that you've set the webhook URL on the WalletPay website to match the WEBHOOK_HOST and WEBHOOK_PATH in your code. Additionally, your server must have an SSL certificate issued by trusted certificate authorities (CA), such as Let's Encrypt. Self-signed certificates will not be accepted by WalletPay.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Contact

For any questions or feedback, please reach out to [@xdownedx](https://t.me/xdownedx) on Telegram.
