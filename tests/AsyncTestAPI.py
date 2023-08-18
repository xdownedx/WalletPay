import pytest
from aioresponses import aioresponses
from WalletPay.types import Order
from WalletPay import AsyncWalletPayAPI


@pytest.mark.asyncio
async def test_create_order():
    with aioresponses() as mocked:
        mocked.post('https://pay.wallet.tg/wpay/store-api/v1/order',
                    payload={
                      "status": "SUCCESS",
                      "message": "",
                      "data": {
                        "id": 2703383946854401,
                        "status": "ACTIVE",
                        "number": "9aeb581c",
                        "amount": {
                          "currencyCode": "USD",
                          "amount": "1.00"
                        },
                        "createdDateTime": "2019-08-24T14:15:22Z",
                        "expirationDateTime": "2019-08-24T14:15:22Z",
                        "completedDateTime": "2019-08-24T14:15:22Z",
                        "payLink": "https://t.me/wallet?startattach=wpay_order_2703383946854401",
                        "directPayLink": "https://t.me/wallet/start?startapp=wpay_order-orderId__2703383946854401"
                      }
                    },
                    status=200)

        api = AsyncWalletPayAPI(api_key="test_key")
        order = await api.create_order(
            amount=1.0,
            currency_code="USD",
            description="VPN for 1 month",
            external_id="ORD-5023-4E89",
            timeout_seconds=10800,
            customer_telegram_user_id="0"
        )

        assert isinstance(order, Order)


@pytest.mark.asyncio
async def test_get_order_preview():
    with aioresponses() as mocked:
        mocked.get('https://pay.wallet.tg/wpay/store-api/v1/order/preview?id=2703383946854401',
                   payload={
                      "status": "SUCCESS",
                      "message": "",
                      "data": {
                        "id": 2703383946854401,
                        "status": "ACTIVE",
                        "number": "9aeb581c",
                        "amount": {
                          "currencyCode": "USD",
                          "amount": "1.00"
                        },
                        "createdDateTime": "2019-08-24T14:15:22Z",
                        "expirationDateTime": "2019-08-24T14:15:22Z",
                        "completedDateTime": "2019-08-24T14:15:22Z",
                        "payLink": "https://t.me/wallet?startattach=wpay_order_2703383946854401",
                        "directPayLink": "https://t.me/wallet/start?startapp=wpay_order-orderId__2703383946854401"
                      }
                    },
                   status=200)

        api = AsyncWalletPayAPI(api_key="test_key")
        order = await api.get_order_preview(order_id="2703383946854401")

        assert isinstance(order, Order)
