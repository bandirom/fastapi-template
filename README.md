# FastApi project

* Install dependencies
```shell
poetry install
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
