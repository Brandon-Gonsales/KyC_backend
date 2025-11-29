import asyncio
import sys
import os

# Add the current directory to sys.path so we can import app
sys.path.append(os.getcwd())

from app.db.database import estudiante_collection

async def test_connection():
    print("Testing connection using app.db.database...")
    try:
        # Try to find one document or just check connection
        # We use a simple command that requires auth and connection
        count = await estudiante_collection.count_documents({})
        print(f"SUCCESS: Connected! Found {count} documents in 'estudiantes' collection.")
    except Exception as e:
        print(f"FAILURE: Could not connect.")
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_connection())
