from datetime import datetime
from decimal import Decimal


class Expense:
    def __init__(
        self, session_id: int, user_id: int, amount: Decimal, description: str = None
    ):
        self.id = None
        self.session_id = session_id
        self.user_id = user_id
        self.amount = amount
        self.description = description
        self.date = datetime.now()

    def to_dict(self):
        return {
            "id": self.id,
            "session_id": self.session_id,
            "user_id": self.user_id,
            "amount": float(self.amount),
            "description": self.description,
            "date": self.date.isoformat(),
        }

    @classmethod
    def from_dict(cls, data):
        expense = cls(
            session_id=data["session_id"],
            user_id=data["user_id"],
            amount=Decimal(str(data["amount"])),
            description=data.get("description"),
        )
        expense.id = data.get("id")
        expense.date = (
            datetime.fromisoformat(data["date"])
            if isinstance(data["date"], str)
            else data["date"]
        )
        return expense
