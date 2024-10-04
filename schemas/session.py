from datetime import datetime
from typing import List

from pydantic import BaseModel


class Participant(BaseModel):
    walletAddress: str
    joined: bool


class SessionCreate(BaseModel):
    id: int
    state: str
    fiat: str
    qty_users: int
    participants: List[Participant]


class SessionResponse(BaseModel):
    id: int
    created_at: datetime
    state: str
    fiat: str
    total_spent: float
    qty_users: int


class JoinSessionRequest(BaseModel):
    walletAddress: str
