import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.di import Container
from src.config import app_config


logger = logging.getLogger(__name__)

container = Container()
container.wire(modules=[])

app = FastAPI(title="MTrack API", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=app_config.cors_origins,
    allow_credentials=app_config.cors_allow_credentials,
    allow_methods=app_config.cors_allow_methods,
    allow_headers=app_config.cors_allow_headers,
)

