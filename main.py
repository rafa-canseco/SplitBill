from typing import Dict, List, Optional, Union

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .models.expense import Expense
from .models.session import Session
from .schemas.expense import ExpenseCreate, ExpenseResponse
from .schemas.session import JoinSessionRequest, SessionCreate, SessionResponse
from .schemas.user import UserCreate, UserResponse, UserUpdate
from .services.expense_service import create_multiple_expenses
from .services.session_balance_service import checkout_session
from .services.session_service import (
    create_session,
    get_sessions_by_wallet_address,
    join_session,
)
from .services.user_service import (
    check_user_by_privy_id,
    check_user_by_wallet,
    create_user,
    get_user_by_privy_id,
    update_user,
)

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


@app.get("/api/user/check")
def check_user_endpoint(
    privy_id: Optional[str] = None, wallet_address: Optional[str] = None
) -> Dict[str, Union[bool, Optional[str]]]:
    if not privy_id and not wallet_address:
        raise HTTPException(
            status_code=400, detail="Either privy_id or wallet_address must be provided"
        )

    user: Optional[UserResponse] = None
    if privy_id:
        user = check_user_by_privy_id(privy_id)
    if not user and wallet_address:
        user = check_user_by_wallet(wallet_address)

    if user:
        return {
            "isRegistered": user.is_profile_complete,
            "isInvited": user.is_invited,
            "walletAddress": user.walletAddress,
        }
    return {"isRegistered": False, "isInvited": False, "walletAddress": None}


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
            is_invited=user_data.is_invited,
        )
        return user
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/api/user/{privy_id}", response_model=UserResponse)
def update_user_endpoint(privy_id: str, user_data: UserUpdate):
    try:
        updated_user = update_user(privy_id, user_data.dict(exclude_unset=True))
        return UserResponse(**updated_user.__dict__)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/create_session", response_model=SessionResponse)
def create_session_endpoint(session_data: SessionCreate):
    new_session = Session(
        id=session_data.id,
        state=session_data.state,
        fiat=session_data.fiat,
        qty_users=session_data.qty_users,
    )
    created_session = create_session(new_session, session_data.participants)

    return SessionResponse(**created_session.to_dict())


@app.post("/create_expense", response_model=List[ExpenseResponse])
def create_expense_endpoint(expenses_data: ExpenseCreate):
    try:
        created_expenses = create_multiple_expenses(
            expenses_data.session_id, expenses_data.expenses
        )
        expense_objects = [Expense.from_dict(expense) for expense in created_expenses]
        return [ExpenseResponse(**expense.to_dict()) for expense in expense_objects]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@app.post("/sessions/{session_id}/checkout")
async def checkout_session_endpoint(session_id: int):
    try:
        result = checkout_session(session_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/sessions/{session_id}/join")
async def join_session_endpoint(session_id: int, join_request: JoinSessionRequest):
    try:
        result = join_session(session_id, join_request.walletAddress)
        return {"message": "Successfully joined the session", "data": result}
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
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
