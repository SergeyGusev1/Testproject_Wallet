import os
import sys


from app.models.wallet import Wallet # noqa
from app.core.config import settings
from app.core.db import Base
from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

sys.path.append(os.path.dirname(os.path.dirname(__file__)))


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config
database_url = settings.database_url
print(f"Original URL from settings: {database_url}")  # для отладки

# 🔥 ЗАМЕНЯЕМ АСИНХРОННЫЙ ДРАЙВЕР НА СИНХРОННЫЙ
if database_url.startswith("postgresql+asyncpg:"):
    sync_url = database_url.replace("postgresql+asyncpg:", "postgresql:")
    print(f"Using SYNC URL for migrations: {sync_url}")
else:
    sync_url = database_url

# Устанавливаем синхронный URL для Alembic
config.set_main_option("sqlalchemy.url", sync_url)
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
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
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

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
