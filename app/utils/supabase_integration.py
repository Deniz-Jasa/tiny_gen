import os
from supabase import create_client, Client
from typing import Dict
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize the Supabase client
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def store(table_name: str, data: Dict):
    """Inserts data into the specified Supabase table."""
    response = supabase.table(table_name).insert(data).execute()
    return response
