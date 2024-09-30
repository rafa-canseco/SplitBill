from pydantic import BaseModel,Field
from decimal import Decimal
from datetime import datetime
from typing import Optional,List

class UserExpense(BaseModel):
    user_id: int
    amount: Decimal = Field(..., ge=0)
    description: Optional[str] = None
    
class ExpenseCreate(BaseModel):
    session_id: int
    expenses: List[UserExpense]
    
class ExpenseResponse(BaseModel):
    id: int
    session_id: int
    user_id: int
    amount: Decimal
    description: Optional[str]
    date: datetime
    