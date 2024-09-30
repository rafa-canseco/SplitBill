from fastapi import FastAPI,HTTPException

from .models.user import User
from .models.session import Session
from .models.expense import Expense
from .services.user_service import create_user
from .services.session_service import create_session
from .services.expense_service import create_expense,create_multiple_expenses
from .services.session_balance_service import checkout_session
from .schemas.user import UserCreate,userResponse
from .schemas.session import SessionCreate,SessionResponse
from .schemas.expense import ExpenseCreate,ExpenseResponse
from typing import List

app = FastAPI()

@app.get("/")
def read_root():
    return {"hello": "world"}

@app.post("/create_user")
def create_user_endpoint(user:UserCreate):
    new_user = User(**user.dict())
    created_user = create_user(new_user)
    return created_user
    
@app.post("/create_session", response_model=SessionResponse)
def create_session_endpoint(session_data:SessionCreate):
    new_session = Session(
        state = session_data.state,
        fiat = session_data.fiat,
        qty_users = session_data.qty_users,
    )
    created_session = create_session(new_session, session_data.users_ids)
    
    return SessionResponse(**created_session.to_dict())

@app.post("/create_expense", response_model=List[ExpenseResponse])
def create_expense_endpoint(expenses_data: ExpenseCreate):
    try:
        created_expenses = create_multiple_expenses(expenses_data.session_id, expenses_data.expenses)
        expense_objects = [Expense.from_dict(expense) for expense in created_expenses]
        return [ExpenseResponse(**expense.to_dict()) for expense in expense_objects]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
        
@app.post("/sessions/{session_id}/checkout")
async def checkout_session_endpoint(session_id: int):
    try:
        print("enteresd")
        result = checkout_session(session_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
                
    
    