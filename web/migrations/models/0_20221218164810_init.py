from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "user" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "first_name" VARCHAR(150) NOT NULL  DEFAULT '',
    "last_name" VARCHAR(150) NOT NULL  DEFAULT '',
    "email" VARCHAR(150) NOT NULL UNIQUE,
    "password" VARCHAR(200) NOT NULL,
    "is_active" INT NOT NULL  DEFAULT 0,
    "is_admin" INT NOT NULL  DEFAULT 0,
    "date_joined" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSON NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
