from typing import List, Dict
from decimal import Decimal
from ..database.supabase_client import supabase


def checkout_session(session_id: int) -> Dict:
    try:
        session_response = supabase.table("sessions").select("total_spent").eq("id",session_id).execute()
        if not session_response.data:
                raise ValueError(f"No se encontró la sesión con id {session_id}")
        total_spent = Decimal(str(session_response.data[0]['total_spent']))

        users_response = supabase.table("sessions_users").select("user_id,total_spent").eq("session_id",session_id).execute()
        if not users_response.data:
                raise ValueError(f"No se encontraron usuarios para la sesión {session_id}")

        user_ids = [user['user_id'] for user in users_response.data]
        users_info = supabase.table("users").select("id,name,email,walletAddress").in_("id", user_ids).execute()
        users_info_dict = {user['id']: user for user in users_info.data}

        users_spent = {user['user_id']: Decimal(str(user['total_spent'])) for user in users_response.data}
        num_users = len(users_spent)

        fair_share = total_spent / num_users
        print(fair_share)

        balances = {user_id: spent - fair_share for user_id, spent in users_spent.items()}
        print(balances)

        payers = {user_id: -balance for user_id, balance in balances.items() if balance < 0}
        receivers = {user_id: balance for user_id, balance in balances.items() if balance > 0}

        supabase.table("sessions").update({"state": "waiting_payment"}).eq("id", session_id).execute()

        return {
            "session_id": session_id,
            "total_spent": float(total_spent),
            "fair_share": float(fair_share),
            "payers": {str(k): {"amount": float(v), "name": users_info_dict[k]['name'], "email": users_info_dict[k]['email'], "walletAddress": users_info_dict[k]['walletAddress']} for k, v in payers.items()},
            "receivers": {str(k): {"amount": float(v), "name": users_info_dict[k]['name'], "email": users_info_dict[k]['email'], "walletAddress": users_info_dict[k]['walletAddress']} for k, v in receivers.items()}
        }

    except Exception as e:
        print(f"Error en checkout_session: {str(e)}")
        raise