import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from os import getenv
from dotenv import load_dotenv
import ssl

load_dotenv()

async def test_connection(name, **kwargs):
    mongo_url = getenv("MONGO_URL")
    print(f"\n--- Testing {name} ---")
    try:
        client = AsyncIOMotorClient(mongo_url, **kwargs)
        # Force a connection attempt
        await client.admin.command('ping')
        print(f"SUCCESS: Connected using {name}")
        return True
    except Exception as e:
        print(f"FAILURE: Could not connect using {name}")
        print(f"Error: {e}")
        return False

async def main():
    print("Starting SSL Diagnostic...")
    
    # 1. Test Standard Connection
    await test_connection("Standard Connection")

    # 2. Test with certifi (if available)
    try:
        import certifi
        print(f"\nCertifi found at: {certifi.where()}")
        await test_connection("Certifi CA Bundle", tlsCAFile=certifi.where())
    except ImportError:
        print("\nCertifi not installed, skipping certifi test.")

    # 3. Test with tlsAllowInvalidCertificates=True (INSECURE - for testing only)
    await test_connection("Insecure (tlsAllowInvalidCertificates=True)", tlsAllowInvalidCertificates=True)

if __name__ == "__main__":
    asyncio.run(main())
