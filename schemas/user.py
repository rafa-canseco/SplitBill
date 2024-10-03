from typing import Optional

from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    privy_id: str
    name: str
    email: str
    walletAddress: str
    is_invited: bool


class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    walletAddress: Optional[str] = None


class UserResponse(BaseModel):
    id: int
    name: Optional[str] = None
    email: Optional[str] = None
    walletAddress: str
    privy_id: Optional[str] = None
    is_profile_complete: bool = Field(default=False)
    is_invited: bool = Field(default=False)


class UserCheck(BaseModel):
    privy_id: str
