from pydantic import BaseModel

class Amount(BaseModel):
    currencyCode: str
    amount: str

class SelectedPaymentOption(BaseModel):
    amount: Amount
    amountFee: Amount
    amountNet: Amount
    exchangeRate: str

class Payload(BaseModel):
    id: int
    number: str
    externalId: str
    customData: str
    orderAmount: Amount
    selectedPaymentOption: SelectedPaymentOption
    orderCompletedDateTime: str

class WebhookData(BaseModel):
    eventDateTime: str
    eventId: int
    type: str
    payload: Payload
