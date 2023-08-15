from typing import Dict
class Order:
    def __init__(self, data: Dict):
        self.id = data["id"]
        self.status = data["status"]
        self.number = data["number"]
        self.amount = data["amount"]
        self.created_date_time = data["createdDateTime"]
        self.expiration_date_time = data["expirationDateTime"]
        self.completed_date_time = data["completedDateTime"]
        self.pay_link = data["payLink"]
        self.direct_pay_link = data["directPayLink"]

    def __str__(self) -> str:
        return f"Order(id={self.id}, status={self.status}, number={self.number}, amount={self.amount})"
