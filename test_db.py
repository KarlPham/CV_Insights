import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Try to connect to PostgreSQL
try:
    conn = psycopg2.connect(os.getenv("DATABASE_URL"))
    print("✅ Database connection successful!")
    conn.close()

except Exception as e:
    print("❌ Failed to connect to the database")
    print(f"Error: {e}")