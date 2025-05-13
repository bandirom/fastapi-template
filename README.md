# FastApi Template project

**Useful links:**

- [FastAPI](https://fastapi.tiangolo.com/)
- [Poetry dependencies](https://python-poetry.org/docs/managing-dependencies/))

## Installation

* Clone the repository

```shell
git clone https://github.com/bandirom/fastapi-template.git
```

* Install dependencies for local development

```shell
poetry install --extras dev
```

* Create `.env` file

```dotenv
DATABASE_URI="postgresql+asyncpg://develop:develop@localhost/develop"
DEBUG=1
SECRET_KEY="someSecret"
```

## Run project

* Up only Postgresql and Redis in docker compose

```shell
docker-compose up -d db redis
```

* Run project

```shell
python main.py
```

## Use Alembic for migrations

* Init alembic (Already done in the project)

```shell
alembic init -t async alembic
```

* Check if Alembic works well

```shell
alembic current
```

* Generate migrations

```shell
alembic revision --autogenerate -m "migration_name"
```

* Migrate

```shell
alembic upgrade head
```

---

### Work with async DB

* Get users

```python
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from db.models import User


async def get_users(session: AsyncSession):
  result = await session.execute(select(User))
  return result.scalars().all()
```

---

## Docker & docker compose

### Local development with docker compose

* Edit `.env` file

```dotenv
DATABASE_URI=postgresql+asyncpg://develop:develop@db/develop
```

* Build docker compose image

```shell
docker compose up -d --build
```

### Production

* Build image
```shell
docker build -t fastapi-project -f docker/Dockerfile .
```

* (Optional) Run container
```shell
docker run --rm -it --env-file .env -p 8080:8080 --name fastapi-project fastapi-project
```
