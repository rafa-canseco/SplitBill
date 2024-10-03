from typing import List

from fastapi import HTTPException

from ..database.supabase_client import supabase
from ..models.user import User
from ..schemas.user import UserResponse


def check_user_exists(privy_id: str) -> bool:
    response = supabase.table("users").select("id").eq("privy_id", privy_id).execute()
    print(response.data)
    return len(response.data) > 0


def get_user_by_privy_id(privy_id: str) -> UserResponse:
    response = supabase.table("users").select("*").eq("privy_id", privy_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponse(**response.data[0])


def create_user(
    privy_id: str, name: str, email: str, walletAddress: str
) -> UserResponse:
    new_user_data = {
        "privy_id": privy_id,
        "name": name,
        "email": email,
        "walletAddress": walletAddress,
        "is_profile_complete": True,
    }

    response = supabase.table("users").insert(new_user_data).execute()

    if not response.data:
        raise HTTPException(status_code=500, detail="Failed to create user")

    created_user_id = response.data[0]["id"]

    user_response = (
        supabase.table("users").select("*").eq("id", created_user_id).execute()
    )

    if not user_response.data:
        raise HTTPException(status_code=500, detail="Failed to retrieve created user")

    user_data = user_response.data[0]

    try:
        user_response = UserResponse(
            id=user_data["id"],
            privy_id=user_data["privy_id"],
            name=user_data["name"],
            email=user_data["email"],
            walletAddress=user_data["walletAddress"],
            is_profile_complete=user_data["is_profile_complete"],
        )
        return user_response
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error creating UserResponse: {str(e)}"
        )


def update_user(privy_id: str, data: dict) -> User:
    response = supabase.table("users").update(data).eq("privy_id", privy_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="User not found")
    return User(**response.data[0])


def user_exists(user_id):
    response = supabase.table("users").select("id").eq("id", user_id).execute()
    return len(response.data) > 0


def get_or_create_users(wallet_addresses: List[str]) -> List[int]:
    user_ids = []
    for wallet in wallet_addresses:
        user_response = (
            supabase.table("users").select("id").eq("walletAddress", wallet).execute()
        )

        if user_response.data:
            user_ids.append(user_response.data[0]["id"])
        else:
            new_user_response = (
                supabase.table("users").insert({"walletAddress": wallet}).execute()
            )

            if new_user_response.data:
                user_ids.append(new_user_response.data[0]["id"])
            else:
                raise Exception(f"Failed to create user for wallet: {wallet}")

    return user_ids
