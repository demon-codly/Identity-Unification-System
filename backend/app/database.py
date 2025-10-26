"""
Supabase database client initialization
"""
from supabase import create_client, Client
from app.config import Config


class SupabaseClient:
    """Singleton Supabase client"""
    
    _instance: Client = None
    
    @classmethod
    def get_client(cls) -> Client:
        """Get or create Supabase client instance"""
        if cls._instance is None:
            if not Config.SUPABASE_URL or not Config.SUPABASE_KEY:
                raise ValueError("Supabase credentials not configured")
            
            cls._instance = create_client(
                Config.SUPABASE_URL,
                Config.SUPABASE_KEY
            )
        
        return cls._instance


# Export singleton instance
def get_db() -> Client:
    """Get Supabase database client"""
    return SupabaseClient.get_client()
