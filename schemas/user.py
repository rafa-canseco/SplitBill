from typing import Optional

from pydantic import BaseModel


class UserCreate(BaseModel):
    privy_id: str
    name: str
    email: str
    walletAddress: str


class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    walletAddress: Optional[str] = None


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    walletAddress: str
    privy_id: str
    is_profile_complete: bool


class UserCheck(BaseModel):
    privy_id: str
