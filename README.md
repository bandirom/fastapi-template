# FastAPI template project

## Aerich:

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


