import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.di import Container
from src.config.app_config import app_config

from src.routers import transactions, dashboard, categories


logger = logging.getLogger(__name__)

container = Container()
container.wire(modules=[transactions, dashboard, categories])

app = FastAPI(title="MTrack API", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=app_config.cors_origins,
    allow_credentials=app_config.cors_allow_credentials,
    allow_methods=app_config.cors_allow_methods,
    allow_headers=app_config.cors_allow_headers,
)

app.include_router(transactions.api_router, prefix="/api/v1/transactions", tags=["transactions"])
app.include_router(dashboard.api_router, prefix="/api/v1/dashboard", tags=["dashboard"])
app.include_router(categories.api_router, prefix="/api/v1/categories", tags=["categories"])