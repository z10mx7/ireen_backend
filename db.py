import motor.motor_asyncio
import sys

server_path = "mongodb://mongo_user:mongo_password@mongo:27017/"

client = motor.motor_asyncio.AsyncIOMotorClient(server_path, serverSelectionTimeoutMS=5000)
