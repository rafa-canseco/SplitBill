from typing import List, Optional

from fastapi import HTTPException

from ..database.supabase_client import supabase
from ..models.user import User
from ..schemas.user import UserResponse


def check_user_by_privy_id(privy_id: str) -> Optional[UserResponse]:
    response = supabase.table("users").select("*").eq("privy_id", privy_id).execute()
    if response.data:
        return UserResponse(**response.data[0])
    return None


def check_user_by_wallet(wallet_address: str) -> Optional[UserResponse]:
    response = (
        supabase.table("users")
        .select("*")
        .eq("walletAddress", wallet_address)
        .execute()
    )
    if response.data:
        return UserResponse(**response.data[0])
    return None


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
    privy_id: str, name: str, email: str, walletAddress: str, is_invited: bool
) -> UserResponse:
    existing_user = (
        supabase.table("users")
        .select("*")
        .eq("walletAddress", walletAddress)
        .eq("is_invited", True)
        .execute()
    )

    user_data = {
        "privy_id": privy_id,
        "name": name,
        "email": email,
        "walletAddress": walletAddress,
        "is_profile_complete": True,
        "is_invited": is_invited,
    }

    if existing_user.data:
        user_id = existing_user.data[0]["id"]
        response = supabase.table("users").update(user_data).eq("id", user_id).execute()
    else:
        response = supabase.table("users").insert(user_data).execute()

    if not response.data:
        raise HTTPException(status_code=500, detail="Failed to create or update user")

    created_or_updated_user = response.data[0]

    try:
        user_response = UserResponse(
            id=created_or_updated_user["id"],
            privy_id=created_or_updated_user["privy_id"],
            name=created_or_updated_user["name"],
            email=created_or_updated_user["email"],
            walletAddress=created_or_updated_user["walletAddress"],
            is_profile_complete=created_or_updated_user["is_profile_complete"],
            is_invited=created_or_updated_user["is_invited"],
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
                supabase.table("users")
                .insert({"walletAddress": wallet, "is_invited": True})
                .execute()
            )

            if new_user_response.data:
                user_ids.append(new_user_response.data[0]["id"])
            else:
                raise Exception(f"Failed to create user for wallet: {wallet}")

    return user_ids
