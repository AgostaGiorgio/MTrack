import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from src.di import Container
from src.config.app_config import app_config
from src.clients.orbit_client import OrbitClient
from src.routers import transactions, dashboard, categories


if app_config.orbit_api_url:
    orbit_client = OrbitClient(
        orbit_api_url=app_config.orbit_api_url,
        name="MTrack",
        version="2.1.0",
        description="Expenses tracker",
        app_url="https://mtrack.agogi.dev"
    )
    
@asynccontextmanager
async def lifespan(app: FastAPI):
    if app_config.orbit_api_url:
        orbit_client.start()
        yield
        orbit_client.stop()

logger = logging.getLogger(__name__)

container = Container()
container.wire(modules=[transactions, dashboard, categories])

app = FastAPI(lifespan=lifespan, title="MTrack API", version="2.1.0")

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