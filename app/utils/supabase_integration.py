from supabase import create_client, Client
from typing import Dict

# Initialize the Supabase client
SUPABASE_URL = 'https://nzkakblmukwgdoyofzrj.supabase.co'
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im56a2FrYmxtdWt3Z2RveW9menJqIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTcxMDIxMTIwNSwiZXhwIjoyMDI1Nzg3MjA1fQ.yvwgk9TeAPpW3GQWOHUExV-qBkMh-lanbKs9DJmxA_Y'
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def store(table_name: str, data: Dict):
    """Inserts data into the specified Supabase table."""
    response = supabase.table(table_name).insert(data).execute()
    return response