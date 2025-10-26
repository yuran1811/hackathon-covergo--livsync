from supabase import Client, create_client, create_async_client
from supabase.client import ClientOptions

from app.dependencies.config import SUPABASE_KEY, SUPABASE_URL

url: str = SUPABASE_URL or ""
key: str = SUPABASE_KEY or ""
supabase_client: Client = create_client(
    url,
    key,
    options=ClientOptions(
        schema="public",
    ),
)