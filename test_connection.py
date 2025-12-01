import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os
import certifi

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")
DATABASE_NAME = os.getenv("DATABASE_NAME")

print("Probando conexion a MongoDB...")
print(f"URL: {MONGO_URL[:30]}... (truncada por seguridad)")
print(f"Database: {DATABASE_NAME}")

async def test_connection():
    try:
        print("\nIntentando conectar...")
        client = AsyncIOMotorClient(
            MONGO_URL, 
            tlsCAFile=certifi.where(),
            serverSelectionTimeoutMS=5000  # 5 segundos de timeout
        )
        
        # Intentar hacer ping al servidor
        await client.admin.command('ping')
        print("EXITO: Conexion exitosa!")
        
        # Listar las bases de datos
        db_list = await client.list_database_names()
        print(f"\nBases de datos disponibles: {db_list}")
        
        # Verificar la base de datos específica
        db = client[DATABASE_NAME]
        collections = await db.list_collection_names()
        print(f"\nColecciones en '{DATABASE_NAME}': {collections}")
        
        client.close()
        
    except Exception as e:
        print(f"\nERROR al conectar:")
        print(f"   Tipo: {type(e).__name__}")
        print(f"   Mensaje: {str(e)}")
        
        if "DNS" in str(e):
            print("\nSugerencias:")
            print("   1. Verifica que la URL del cluster sea correcta en MongoDB Atlas")
            print("   2. Asegurate de que el cluster existe y esta activo")
            print("   3. Verifica tu conexion a internet")

if __name__ == "__main__":
    asyncio.run(test_connection())
