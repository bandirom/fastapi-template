# FastApi project

* Install dependencies
```shell
poetry install
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
or 
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
result = await session.execute(select(User))
users = result.scalars().all()
```
