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

def store(data: Dict) -> Dict:
    """
    Inserts data into the 'requests' Supabase table and returns the response.

    Parameters:
    - table_name (str): The name of the Supabase table where data will be stored.
    - data (Dict): A dictionary of data to be inserted into the table.

    Returns:
    - Dict: The response from the Supabase insert operation, typically including details of the inserted data.
    """
    response = supabase.table("requests").insert(data).execute()
    return response
