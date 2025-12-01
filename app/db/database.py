import motor.motor_asyncio
from os import getenv
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = getenv("MONGO_URL")
DATABASE_NAME = getenv("DATABASE_NAME")

if not MONGO_URL or not DATABASE_NAME:
    raise Exception("Las variables MONGO_URL y DATABASE_NAME deben estar definidas en el archivo .env")

import certifi

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL, tlsCAFile=certifi.where())
database = client[DATABASE_NAME]
estudiante_collection = database.get_collection("estudiantes")
