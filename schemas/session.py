from pydantic import BaseModel
from datetime import datetime
from typing import List

class SessionCreate(BaseModel):
    state: str
    fiat: str
    qty_users: int
    users_ids: List[int]

class SessionResponse(BaseModel):
    id: int
    created_at: datetime
    state: str
    fiat: str
    total_spent: float
    qty_users: int