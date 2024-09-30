from ..database.supabase_client import supabase
from ..models.user import User
from datetime import datetime
from fastapi import HTTPException

def create_user(user:User):
    existing_user = supabase.table("users").select("*").eq("address", user.address).execute()
    if existing_user.data:
        raise HTTPException(status_code=400, detail="User address already exists")
        
    data = {
        "name" : user.name,
        "address" : user.address,
        "email" : user.email
    }
    response = supabase.table("users").insert(data).execute()
    if response.data:
        user.id = response.data[0]["id"]
    return user
    
def user_exists(user_id):
    response = supabase.table("users").select("id").eq("id", user_id).execute()
    return len(response.data) > 0
