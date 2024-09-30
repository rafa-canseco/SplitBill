from typing import List
from ..database.supabase_client import supabase
from ..models.expense import Expense
from decimal import Decimal
from ..schemas.expense import UserExpense
from datetime import datetime

def create_expense(expense: Expense):
    data = expense.to_dict()
    del data['id']
    response = supabase.table("expenses").insert(data).execute()
    if response.data:
        expense.id = response.data[0]['id']
    return expense

def create_expenses(session_id: int, user_expenses: List[UserExpense], timestamp: str):
    expenses_data = [
        {
            "session_id": session_id,
            "user_id": expense.user_id,
            "amount": float(expense.amount),
            "description": expense.description,
            "date": timestamp
        }
        for expense in user_expenses
    ]
    return supabase.table("expenses").insert(expenses_data).execute()
    
def update_session_total(session_id: int, new_expenses_total: Decimal):
    session_response = supabase.table("sessions").select("total_spent").eq("id", session_id).execute()
    current_total_spent = Decimal(str(session_response.data[0].get('total_spent', '0')))
    new_total_spent = current_total_spent + new_expenses_total
    supabase.table("sessions").update({"total_spent": float(new_total_spent)}).eq("id", session_id).execute()
    
def update_user_total(session_id: int, user_id: int, amount: Decimal, timestamp: str):
    current_user_data = supabase.table("sessions_users").select("*").eq("session_id", session_id).eq("user_id", user_id).execute()
    
    if current_user_data.data:
        new_total_spent = Decimal(current_user_data.data[0]['total_spent']) + amount
        supabase.table("sessions_users").update({
            "total_spent": float(new_total_spent),
            "last_update": timestamp
        }).eq("session_id", session_id).eq("user_id", user_id).execute()
    else:
        supabase.table("sessions_users").insert({
            "session_id": session_id,
            "user_id": user_id,
            "total_spent": float(amount),
            "last_update": timestamp
        }).execute()
    
def create_multiple_expenses(session_id: int, user_expenses:List[UserExpense]):
    current_timestamp = datetime.utcnow().isoformat()
    try:
        expenses_response = create_expenses(session_id, user_expenses, current_timestamp)

        new_expenses_total = Decimal(sum(Decimal(str(expense.amount)) for expense in user_expenses))
        update_session_total(session_id, new_expenses_total)
        
        for expense in user_expenses:
            update_user_total(session_id, expense.user_id, Decimal(str(expense.amount)), current_timestamp)
        
        return expenses_response.data
    except Exception as e:
        print(f"Error in create_multiple_expenses: {str(e)}")
        raise
        
