from fastapi import APIRouter, Depends, HTTPException, Query
from dependency_injector.wiring import inject, Provide
from src.di import Container
from uuid import UUID


api_router = APIRouter()
