import os

import sqlalchemy
from dotenv import load_dotenv

from alembic import config, script
from alembic.runtime import migration

load_dotenv()

DATABASE_URI = os.getenv('DATABASE_URI')


def test_check():
    assert 2 == 2
