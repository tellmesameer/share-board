from logging.config import fileConfig
from sqlalchemy import create_engine, pool
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from alembic import context
import asyncio
import os
from dotenv import load_dotenv
# Import your models
from app.models import Base  # Adjust this import based on your project structure
load_dotenv()
# Load the Alembic Config object
config = context.config

# Interpret the config file for logging
if config.config_file_name:
    fileConfig(config.config_file_name)

# Set target metadata for migrations
target_metadata = Base.metadata

# Define database URL (ensure this matches your async setup)
DATABASE_URL = os.environ.get("DATABASE_URL")

# Create an async engine
engine = create_async_engine(DATABASE_URL, poolclass=pool.NullPool)


async def run_migrations():
    """Run migrations asynchronously"""
    async with engine.connect() as connection:
        await connection.run_sync(do_run_migrations)


def do_run_migrations(connection):
    """Configure Alembic for migrations"""
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()


if context.is_offline_mode():
    # Running migrations in offline mode
    context.configure(url=DATABASE_URL, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()
else:
    # Running migrations in online mode
    asyncio.run(run_migrations())  # Ensure async migration execution
