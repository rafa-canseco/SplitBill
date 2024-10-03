from datetime import datetime
from typing import List

from pydantic import BaseModel


class SessionCreate(BaseModel):
    state: str
    fiat: str
    qty_users: int
    wallet_addresses: List[str]


class SessionResponse(BaseModel):
    id: int
    created_at: datetime
    state: str
    fiat: str
    total_spent: float
    qty_users: int
