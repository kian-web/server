from fastapi import FastAPI, HTTPException, status
from app.models import docs, schema
from beanie.operators import In
from beanie import init_beanie
from uuid import uuid1
from app.routes import router
from contextlib import asynccontextmanager
from motor.motor_asyncio import AsyncIOMotorClient

config = schema.ConfigModel.model_validate_json(open("config.json").read())


@asynccontextmanager
async def lifespan(app: FastAPI):
    client = AsyncIOMotorClient(str(config.db))
    await init_beanie(database=client.db_name, document_models=docs.DOCUMENTS_LIST)
    yield


app = FastAPI(lifespan=lifespan)
app.config = config
app.include_router(router)
