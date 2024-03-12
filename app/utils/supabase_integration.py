from supabase import create_client, Client
from typing import Dict

# Initialize the Supabase client


def store(table_name: str, data: Dict):
    """Inserts data into the specified Supabase table."""
    response = supabase.table(table_name).insert(data).execute()
    return response
