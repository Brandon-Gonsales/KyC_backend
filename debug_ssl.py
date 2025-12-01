import asyncio
import os
from dotenv import load_dotenv
import motor.motor_asyncio
import certifi
import ssl

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")

async def test_connect(name, **kwargs):
    print(f"Testing {name}...")
    try:
        client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL, serverSelectionTimeoutMS=5000, **kwargs)
        await client.admin.command('ping')
        print(f"SUCCESS: {name}")
    except Exception as e:
        print(f"FAILURE: {name}")
        print(f"Error: {e}")

async def main():
    print(f"Certifi path: {certifi.where()}")
    print(f"Python SSL default context: {ssl.create_default_context().get_ca_certs()}")
    
    # Test 1: Current setup
    await test_connect("Current Setup (certifi)", tlsCAFile=certifi.where())

    # Test 2: No certifi (system defaults)
    await test_connect("System Defaults (no certifi)")

    # Test 3: Insecure
    await test_connect("Insecure (tlsAllowInvalidCertificates=True)", tlsAllowInvalidCertificates=True)

if __name__ == "__main__":
    asyncio.run(main())
