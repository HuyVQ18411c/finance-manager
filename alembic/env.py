import os
from logging.config import fileConfig

from sqlalchemy import create_engine

from alembic import context

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
from financesvc.domain.models import Base

DATABASE_HOST = os.environ.get('DATABASE_HOST', 'localhost')
DATABASE_USERNAME = os.environ.get('DATABASE_USERNAME', 'admin')
DATABASE_PORT = int(os.environ.get('DATABASE_PORT', '45432'))
DATABASE_PASSWORD = os.environ.get('DATABASE_PASSWORD', 'EDYRcmEpuF8')
DATABASE_NAME = os.environ.get('DATABASE_NAME', 'finance')

DB_URL = 'postgresql://{username}:{password}@{host}:{port}/{name}'.format(
    username=DATABASE_USERNAME,
    password=DATABASE_PASSWORD,
    host=DATABASE_HOST,
    port=DATABASE_PORT,
    name=DATABASE_NAME
)
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)


target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = DB_URL
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = create_engine(DB_URL)

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
