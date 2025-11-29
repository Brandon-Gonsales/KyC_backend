import asyncio
import os
from dotenv import load_dotenv
import motor.motor_asyncio
import ssl
import certifi

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
    print(f"OpenSSL Version: {ssl.OPENSSL_VERSION}")
    
    # Test 4: Custom SSL Context (TLS 1.2)
    try:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        # Try to set minimum version to TLS 1.2
        ctx.minimum_version = ssl.TLSVersion.TLSv1_2
        
        # Note: motor/pymongo accepts 'tlsAllowInvalidCertificates' etc, but to pass a context we might need 'ssl_context' (older) or just rely on driver.
        # Actually pymongo doesn't easily accept a raw ssl_context object in the URI or kwargs for AsyncIOMotorClient directly in all versions.
        # But we can try passing it if supported, or configure via kwargs.
        # Pymongo 4.x usually manages SSL context itself. 
        # However, we can try to see if we can influence it.
        
        # Actually, let's just print the version and try one more thing:
        # Some users report issues with 'tls=True' missing.
        await test_connect("Explicit tls=True", tls=True, tlsAllowInvalidCertificates=True)
        
    except Exception as e:
        print(f"Error setting up context: {e}")

if __name__ == "__main__":
    asyncio.run(main())
