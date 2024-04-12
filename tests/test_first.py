import os

import sqlalchemy
from dotenv import load_dotenv

from alembic import config, script
from alembic.runtime import migration

load_dotenv()

DATABASE_URI = os.getenv('DATABASE_URI')


def test_check():
    assert 2 == 2


def check_alembic_integrity():
    engine = sqlalchemy.create_engine(DATABASE_URI)
    alembic_cfg = config.Config('alembic.ini')
    script_ = script.ScriptDirectory.from_config(alembic_cfg)
    with engine.begin() as conn:
        context = migration.MigrationContext.configure(conn)
        assert context.get_current_revision() == script_.get_current_head()
