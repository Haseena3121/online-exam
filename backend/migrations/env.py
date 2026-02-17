"""Alembic environment configuration"""

import logging
from sqlalchemy import pool
from alembic import context

from app import create_app
from database import db

# Alembic Config object
config = context.config

# 🚫 Removed fileConfig to avoid 'qualname' logging error
# from logging.config import fileConfig
# fileConfig(config.config_file_name)

logger = logging.getLogger("alembic.env")

def get_engine():
    """Get database engine from Flask app"""
    app = create_app()
    return app.extensions['migrate'].db.get_engine(app)

def get_metadata():
    """Get metadata from models"""
    return db.metadata

def run_migrations_offline():
    """Run migrations in 'offline' mode"""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=get_metadata(),
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Run migrations in 'online' mode"""
    app = create_app()
    with app.app_context():
        connectable = db.engine

        with connectable.connect() as connection:
            context.configure(
                connection=connection,
                target_metadata=get_metadata(),
            )

            with context.begin_transaction():
                context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
