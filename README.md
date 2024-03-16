# FastApi project

* Install dependencies (Source: [poetry](https://python-poetry.org/docs/managing-dependencies/))
```shell
poetry install --with dev
```

* Create `.env` file
```dotenv
DATABASE_URI="postgresql+asyncpg://develop:develop@localhost/develop"
DEBUG=true
SECRET_KEY="someSecret"
```

* Run docker db
```shell
docker-compose up -d
```

* Run project
```shell
uvicorn main:app --reload
```
or
```shell
python main.py
```

## Set up Alembic

* Init alembic
```shell
alembic init -t async alembic
```

* check if Alembic is working well
```shell
alembic current
```

* Generate migrations
```shell
alembic revision --autogenerate -m "Create user"
```

* Migrate
```shell
alembic upgrade head
```


## Work with async DB

* Get users
```python
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from db.models import User

async def get_users(session: AsyncSession):
    result = await session.execute(select(User))
    return result.scalars().all()
```
