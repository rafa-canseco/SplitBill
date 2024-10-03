from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .models.session import Session
from .models.expense import Expense
from .services.user_service import (
    check_user_exists,
    get_user_by_privy_id,
    create_user,
    update_user,
)
from .services.session_service import (
    create_session,
    get_sessions_by_wallet_address,
)
from .services.expense_service import create_multiple_expenses
from .services.session_balance_service import checkout_session
from .schemas.user import UserCreate, UserResponse, UserUpdate
from .schemas.session import SessionCreate, SessionResponse
from .schemas.expense import ExpenseCreate, ExpenseResponse
from typing import List, Dict

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"hello": "world"}


@app.get("/api/user/check/{privy_id}")
def check_user_endpoint(privy_id: str) -> Dict[str, bool]:
    is_registered = check_user_exists(privy_id)
    return {"isRegistered": is_registered}


@app.get("/api/user/{privy_id}", response_model=UserResponse)
def get_user_endpoint(privy_id: str):
    try:
        user = get_user_by_privy_id(privy_id)
        return UserResponse(**user.__dict__)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/user", response_model=UserResponse)
async def create_user_endpoint(user_data: UserCreate) -> UserResponse:
    try:
        user = create_user(
            privy_id=user_data.privy_id,
            name=user_data.name,
            email=user_data.email,
            walletAddress=user_data.walletAddress,
        )
        return user
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/api/user/{privy_id}", response_model=UserResponse)
def update_user_endpoint(privy_id: str, user_data: UserUpdate):
    try:
        updated_user = update_user(
            privy_id, user_data.dict(exclude_unset=True)
        )
        return UserResponse(**updated_user.__dict__)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/create_session", response_model=SessionResponse)
def create_session_endpoint(session_data: SessionCreate):
    new_session = Session(
        state=session_data.state,
        fiat=session_data.fiat,
        qty_users=session_data.qty_users,
    )
    created_session = create_session(new_session, session_data.users_ids)

    return SessionResponse(**created_session.to_dict())


@app.post("/create_expense", response_model=List[ExpenseResponse])
def create_expense_endpoint(expenses_data: ExpenseCreate):
    try:
        created_expenses = create_multiple_expenses(
            expenses_data.session_id, expenses_data.expenses
        )
        expense_objects = [
            Expense.from_dict(expense) for expense in created_expenses
        ]
        return [
            ExpenseResponse(**expense.to_dict()) for expense in expense_objects
        ]
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An error occurred: {str(e)}"
        )


@app.post("/sessions/{session_id}/checkout")
async def checkout_session_endpoint(session_id: int):
    try:
        result = checkout_session(session_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/sessions/{walletAddress}")
def endpoint_sessions_by_wallet_address(walletAddress: str):
    try:
        sessions = get_sessions_by_wallet_address(walletAddress)
        return {"sessions": sessions}
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
