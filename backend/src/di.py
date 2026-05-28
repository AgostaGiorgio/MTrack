from dependency_injector import containers, providers
from src.clients.postgres_client import PostgresClient
from src.config import app_config


class Container(containers.DeclarativeContainer):
    postgres_client = providers.Singleton(PostgresClient, db_url=app_config.postgresql_connection_uri)