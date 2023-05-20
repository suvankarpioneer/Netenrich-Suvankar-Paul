import asyncio
from os import environ

import motor
from beanie import init_beanie

from models.user_model import UserModel


async def database():

    # Create Motor client
    client = motor.motor_asyncio.AsyncIOMotorClient(
        "mongodb://127.0.0.1:27017/tunedin"
    )

    print("Connected to database")
    print(client)

    await init_beanie(
        database = client.tunedin,
        document_models = [
            UserModel
        ]
    )


   