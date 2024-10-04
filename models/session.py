from datetime import datetime


class Session:
    def __init__(self, id: int, state: str, fiat: str, qty_users: int):
        self.id = id
        self.created_at = datetime.now()
        self.state = state
        self.fiat = fiat
        self.total_spent = 0.0
        self.qty_users = qty_users

    def to_dict(self):
        return {
            "id": self.id,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "state": self.state,
            "fiat": self.fiat,
            "total_spent": self.total_spent,
            "qty_users": self.qty_users,
        }

    @classmethod
    def from_dict(cls, data):
        session = cls(
            id=data["id"],
            state=data["state"],
            fiat=data["fiat"],
            qty_users=data["qty_users"],
        )
        session.created_at = datetime.strptime(data["created_at"], "%Y-%m-%d %H:%M:%S")
        session.total_spent = data.get("total_spent", 0.0)
        return session
