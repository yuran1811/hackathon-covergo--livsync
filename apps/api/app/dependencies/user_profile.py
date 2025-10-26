from app.dependencies.supabase import supabase_client


async def create_user_profile(profile_data: dict):
    """
    Create a new user profile in Supabase.
    """
    try:
        response = supabase_client.table("users").insert(profile_data).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        raise Exception(f"Error creating user profile: {str(e)}")


async def get_user_profile(user_id: str):
    """
    Fetch user profile from Supabase based on user_id.
    """
    try:
        response = (
            supabase_client.table("users").select("*").eq("id", user_id).execute()
        )
        return response.data[0] if response.data else None
    except Exception as e:
        raise Exception(f"Error fetching user profile: {str(e)}")


async def update_user_profile(user_id: str, profile_data: dict):
    """
    Update user profile in Supabase based on user_id.
    """
    try:
        response = (
            supabase_client.table("users")
            .update(profile_data)
            .eq("id", user_id)
            .execute()
        )
        return response.data[0] if response.data else None
    except Exception as e:
        raise Exception(f"Error updating user profile: {str(e)}")
