#!/usr/bin/env python3
"""
Database Setup Script
Creates the candidates table in Supabase
"""

import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables
load_dotenv()

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

def setup_database():
    """Create the candidates table and indexes"""

    print("🔧 Setting up database...")
    print(f"📍 Connecting to: {SUPABASE_URL}")

    # Create Supabase client
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

    # SQL to create the table
    sql = """
    CREATE TABLE IF NOT EXISTS candidates (
        id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
        name TEXT NOT NULL,
        email TEXT,
        x_profile JSONB,
        github_profile JSONB,
        linkedin_url TEXT,
        current_title TEXT,
        current_company TEXT,
        experiences JSONB,
        total_years_experience NUMERIC DEFAULT 0,
        education JSONB,
        publications JSONB,
        score JSONB,
        priority_tier TEXT DEFAULT 'low',
        discovered_from TEXT,
        discovery_date TIMESTAMP DEFAULT NOW(),
        last_updated TIMESTAMP DEFAULT NOW(),
        notes TEXT,
        CONSTRAINT priority_tier_check CHECK (priority_tier IN ('low', 'medium', 'high', 'top'))
    );

    CREATE INDEX IF NOT EXISTS idx_candidates_priority_tier ON candidates(priority_tier);
    CREATE INDEX IF NOT EXISTS idx_candidates_score ON candidates((score->>'total_score') DESC);
    """

    try:
        # Execute the SQL using the REST API
        print("\n📝 Creating candidates table...")

        # Use the postgrest RPC or direct SQL execution
        # Note: Supabase Python client doesn't have direct SQL execution
        # We need to use the database URL directly or the Supabase dashboard

        print("\n⚠️  The Supabase Python client doesn't support direct SQL execution.")
        print("\n📋 Please run the following SQL in your Supabase SQL Editor:")
        print("=" * 80)
        print(sql)
        print("=" * 80)
        print("\n📖 Instructions:")
        print("1. Go to https://supabase.com/dashboard")
        print(f"2. Open your project: {SUPABASE_URL}")
        print("3. Click 'SQL Editor' in the left sidebar")
        print("4. Click 'New Query'")
        print("5. Paste the SQL above")
        print("6. Click 'Run' or press Cmd/Ctrl + Enter")
        print("\n✅ After running the SQL, your database will be ready!")

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        return False

    return True

if __name__ == "__main__":
    setup_database()
