from typing import Dict
class Event:
    def __init__ (self, data: Dict):
        self.event_id = data["eventId"]
        self.eventDateTime = data["eventDateTime"]
        self.type = data["type"]
        self.payload = Payload(payload=data["payload"])

class Payload:
    def __init__(self, payload: Dict):
        self.order_id = payload["id"]
        self.order_number = payload["number"]
        self.external_id = payload["externalId"]
        self.custom_data = payload["customData"]
        self.order_completed_datetime = payload["orderCompletedDateTime"]
        self.order_amount = OrderAmount(order_amount=payload["orderAmount"])

class OrderAmount:
    def __init__(self, order_amount: Dict):
        self.amount = order_amount["amount"]
        self.currency_code = order_amount["currencyCode"]

class SelectedPaymentOption:
    def __init__(self, selected_payment_option):
        self.amount = OrderAmount(order_amount=selected_payment_option["amount"])
        self.amount_fee = OrderAmount(order_amount=selected_payment_option["amountFee"])
        self.amount_net = OrderAmount(order_amount=selected_payment_option["amountNet"])
