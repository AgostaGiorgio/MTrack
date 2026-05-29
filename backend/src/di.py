from dependency_injector import containers, providers
from src.clients.postgres_client import PostgresClient
from src.config.app_config import app_config

from src.repositories.dashboard import DashboardRepository
from src.repositories.categories import CategoriesRepository
from src.repositories.transactions import TransactionsRepository
from src.services.dashboard import DashboardService
from src.services.categories import CategoriesService
from src.services.transactions import TransactionsService


class Container(containers.DeclarativeContainer):
    postgres_client = providers.Singleton(PostgresClient, db_url=app_config.postgresql_connection_uri)
    
    dashboard_repository = providers.Factory(DashboardRepository, postgres_client=postgres_client)
    categories_repository = providers.Factory(CategoriesRepository, postgres_client=postgres_client)
    transactions_repository = providers.Factory(TransactionsRepository, postgres_client=postgres_client)

    dashboard_service = providers.Factory(DashboardService, dashboard_repository=dashboard_repository)
    categories_service = providers.Factory(CategoriesService, categories_repository=categories_repository)
    transactions_service = providers.Factory(TransactionsService, transactions_repository=transactions_repository, categories_repository=categories_repository)