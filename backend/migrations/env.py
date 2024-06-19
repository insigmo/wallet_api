from logging.config import fileConfig

import django
from alembic import context
from django.conf import settings
from sqlalchemy import engine_from_config
from sqlalchemy import pool

from utils.global_config import GlobalConfig

if not settings.configured:
    django.setup()

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

from backend.models import Wallet, Transaction, Base  # noqa

global_config = GlobalConfig()
config.set_main_option('sqlalchemy.url', global_config.sqlalchemy_database_uri)
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def process_revision_directives(context, revision, directives):
    if config.cmd_opts.autogenerate:
        script = directives[0]
        if script.upgrade_ops.is_empty():
            directives[:] = []
            print('No changes in schema detected.')


def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            process_revision_directives=process_revision_directives,
            compare_server_default=True
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
