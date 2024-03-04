from fastapi import FastAPI, Request, HTTPException
from .types import Event
from typing import Union
from . import WalletPayAPI, AsyncWalletPayAPI
import logging
import hmac
import base64


logging.basicConfig(level=logging.INFO)


class WebhookManager:
    """
    A manager for handling webhooks from WalletPay.

    Attributes:
        successful_callbacks (list): A list of callback functions to handle successful events.
        failed_callbacks (list): A list of callback functions to handle failed events.
        host (str): The host to run the FastAPI server on.
        port (int): The port to run the FastAPI server on.
        webhook_endpoint (str): The endpoint to listen for incoming webhooks.
        app (FastAPI): The FastAPI application instance.
        ALLOWED_IPS (set): A set of IP addresses allowed to send webhooks.
    """

    ALLOWED_IPS = {"172.255.248.29", "172.255.248.12", "127.0.0.1"}

    def __init__(self, client: Union[WalletPayAPI, AsyncWalletPayAPI], host: str = "0.0.0.0", port: int = 9123,
                 webhook_endpoint: str = "/wp_webhook"):
        """
        Initialize the WebhookManager.

        :param client:
        :param host: The host to run the FastAPI server on. Default is "0.0.0.0".
        :param port: The port to run the FastAPI server on. Default is 9123.
        :param webhook_endpoint: The endpoint to listen for incoming webhooks. Default is "/wp_webhook".
        """
        self.successful_callbacks = []
        self.failed_callbacks = []
        self.host = host
        self.port = port
        self.api_key = client.api_key
        if webhook_endpoint[0] != "/":
            self.webhook_endpoint = f"/{webhook_endpoint}"
        else:
            self.webhook_endpoint = webhook_endpoint

        self.app = FastAPI()

    async def start(self):
        """
        Start the FastAPI server to listen for incoming webhooks.
        """
        if self.app:
            import uvicorn
            self.register_webhook_endpoint()
            logging.info(f"Webhook is listening at https://{self.host}:{self.port}{self.webhook_endpoint}")
            runner = uvicorn.Server(
                config=uvicorn.Config(self.app, host=self.host, port=self.port, access_log=False, log_level="error"))
            await runner.serve()

    def successful_handler(self):
        """
        Decorator to register a callback function for handling successful events.

        :return: Decorator function.
        """

        def decorator(func):
            self.successful_callbacks.append(func)
            return func

        return decorator

    def failed_handler(self):
        """
        Decorator to register a callback function for handling failed events.

        :return: Decorator function.
        """

        def decorator(func):
            self.failed_callbacks.append(func)
            return func

        return decorator

    async def _handle_webhook(self, request: Request):
        """
        Internal method to handle incoming webhooks.

        1. Verifies the IP address of the incoming request.
        2. Verifies the signature of the incoming request.
        3. Processes the webhook data.

        :param request: The incoming request object.
        :return: A dictionary with a message indicating the result of the webhook processing.
        """
        x_forwarded_for = request.headers.get("X-Forwarded-For")
        client_ip = x_forwarded_for or request.client.host
        logging.info(f'Incoming webhook from {client_ip}')
        if client_ip not in self.ALLOWED_IPS:
            logging.info(f'IP {client_ip} not allowed')
            raise HTTPException(status_code=403, detail="IP not allowed")

        data = await request.json()
        raw_body = await request.body()
        headers = request.headers

        signature = headers.get("Walletpay-Signature")
        timestamp = headers.get("WalletPay-Timestamp")
        method = request.method
        path = request.url.path
        message = f"{method}.{path}.{timestamp}.{base64.b64encode(raw_body).decode()}"

        expected_signature = hmac.new(
            bytes(self.api_key, 'utf-8'),
            msg=bytes(message, 'utf-8'),
            digestmod=hmac._hashlib.sha256
        ).digest()

        expected_signature_b64 = base64.b64encode(expected_signature).decode()
        if not hmac.compare_digest(expected_signature_b64, signature):
            logging.info(f'Invalid signature. Expected: {expected_signature_b64} Get from header: {signature}')
            raise HTTPException(status_code=400, detail="Invalid signature")

        event = Event(data[0])
        if event.type == "ORDER_PAID":
            for callback in self.successful_callbacks:
                await callback(event)
            return {"message": "Successful event processed!"}
        elif event.type == "ORDER_FAILED":
            for callback in self.failed_callbacks:
                await callback(event)
            return {"message": "Failed event processed!"}
        else:
            return {"message": "Webhook received with unknown status!"}

    def register_webhook_endpoint(self, endpoint: str = '/wp_webhook'):
        """
        Register the webhook endpoint in the FastAPI application.

        :param endpoint: The endpoint to register. Default is '/wp_webhook'.
        """
        self.app.post(endpoint)(self._handle_webhook)
