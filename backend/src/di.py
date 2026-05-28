from dependency_injector import containers, providers
from src.clients.postgres_client import PostgresClient
from src.config.app_config import app_config

from src.repositories.dashboard import DashboardRepository
from src.services.dashboard import DashboardService


class Container(containers.DeclarativeContainer):
    postgres_client = providers.Singleton(PostgresClient, db_url=app_config.postgresql_connection_uri)
    
    dashboard_repository = providers.Factory(DashboardRepository, postgres_client=postgres_client)
    dashboard_service = providers.Factory(DashboardService, dashboard_repository=dashboard_repository)