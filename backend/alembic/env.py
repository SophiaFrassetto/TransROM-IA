import os
import sys
from logging.config import fileConfig
from urllib.parse import quote_plus

from sqlalchemy import create_engine, pool

from alembic import context

# Add the backend directory to the Python path
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, backend_dir)

# Import Base and models
from apis_app.core.config import get_settings
from apis_app.models.base import BaseModel

settings = get_settings()

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
target_metadata = BaseModel.metadata


def get_url():
    """Construct database URL with proper encoding."""
    user = quote_plus(settings.POSTGRES_USER)
    password = quote_plus(settings.POSTGRES_PASSWORD)
    host = quote_plus(settings.POSTGRES_SERVER)
    port = settings.POSTGRES_PORT
    database = quote_plus(settings.POSTGRES_DB)

    return f"postgresql://{user}:{password}@{host}:{port}/{database}"


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    # Use our custom URL with proper encoding
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = get_url()

    connectable = create_engine(
        configuration["sqlalchemy.url"],
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
