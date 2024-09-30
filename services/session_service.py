from ..database.supabase_client import supabase
from ..models.session import Session
from .user_service import user_exists
from postgrest.exceptions import APIError
from datetime import datetime


def create_session(session: Session, user_ids: list):
    try:
        session_data = session.to_dict()
        del session_data['id']
        session_response = supabase.table("sessions").insert(session_data).execute()

        if not session_response.data:
            raise APIError({"message": "Failed to create session"})

        session.id = session_response.data[0]["id"]

        current_time = datetime.now().isoformat()
        session_users_data = [
            {
                "session_id": session.id,
                "user_id": user_id,
                "last_update": current_time,
                "total_spent": 0
            }
            for user_id in user_ids
        ]

        session_users_response = supabase.table("sessions_users").insert(session_users_data).execute()

        if not session_users_response.data:
            supabase.table("sessions").delete().eq("id", session.id).execute()
            raise APIError({"message": "Failed to add users to session"})

        return session
    except APIError as e:
        raise