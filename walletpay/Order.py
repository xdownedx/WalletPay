class Order:
    def __init__(self, data):
        self.id = data.get("id")
        self.status = data.get("status")
        self.number = data.get("number")
        self.amount = data.get("amount", {})
        self.created_date_time = data.get("createdDateTime")
        self.expiration_date_time = data.get("expirationDateTime")
        self.completed_date_time = data.get("completedDateTime")
        self.pay_link = data.get("payLink")
        self.direct_pay_link = data.get("directPayLink")

    def __str__(self):
        return f"Order(id={self.id}, status={self.status}, number={self.number}, amount={self.amount})"



