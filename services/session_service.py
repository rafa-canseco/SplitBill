from datetime import datetime
from typing import List

from postgrest.exceptions import APIError

from ..database.supabase_client import supabase
from ..models.session import Session
from ..schemas.session import Participant
from ..services.user_service import get_or_create_users


def create_session(session: Session, participants: List[Participant]):
    try:
        session_data = session.to_dict()
        del session_data["id"]
        session_response = supabase.table("sessions").insert(session_data).execute()

        if not session_response.data:
            raise APIError({"message": "Failed to create session"})

        session.id = session_response.data[0]["id"]

        current_time = datetime.now().isoformat()
        session_users_data = [
            {
                "session_id": session.id,
                "user_id": get_or_create_users(participant.walletAddress),
                "last_update": current_time,
                "total_spent": 0,
                "joined": participant.joined,
            }
            for participant in participants
        ]

        session_users_response = (
            supabase.table("sessions_users").insert(session_users_data).execute()
        )

        if not session_users_response.data:
            supabase.table("sessions").delete().eq("id", session.id).execute()
            raise APIError({"message": "Failed to add users to session"})

        return session
    except APIError:
        raise


def get_sessions_by_wallet_address(walletAddress: str):
    try:
        user = (
            supabase.table("users")
            .select("id")
            .eq("walletAddress", walletAddress)
            .single()
            .execute()
        )
        if not user.data:
            raise ValueError("User not found")

        user_id = user.data["id"]

        sessions = (
            supabase.table("sessions_users")
            .select("session_id, sessions(*)")
            .eq("user_id", user_id)
            .execute()
        )
        formatted_sessions = []
        for item in sessions.data:
            session_info = item["sessions"]
            session_info["id"] = item["session_id"]
            formatted_sessions.append(session_info)

        return formatted_sessions
    except Exception as e:
        raise Exception(f"Error getting sessions: {str(e)}")
