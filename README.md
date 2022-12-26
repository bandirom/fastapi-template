# FastAPI template project


### Works with Config.py

---

Pydantic settings has configuration

* `case_sensitive=True`
* `env_nested_delimiter = '__'`


For configure or change project settings you can use `env variables`

Change JWT access token expire time:
```shell
export DEBUG=0
export JWT__ACCESS_TOKEN_EXPIRE_MINUTES=1000
```


### Aerich (DB Migrations manager):

---

* Init db before apply migration:

```shell
aerich init-db
```

* Make a migrations after changes in models:
```shell
aerich migrate --name <migration_name>
```

* Migrate changes:
```shell
aerich upgrade
```
