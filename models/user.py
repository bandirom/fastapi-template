from tortoise import models, fields
from datetime import datetime


class User(models.Model):
    id = fields.IntField(pk=True, index=True)
    first_name = fields.CharField(max_length=150, default='')
    last_name = fields.CharField(max_length=150, default='')
    email = fields.CharField(max_length=150, null=False, unique=True)
    password = fields.CharField(max_length=200, null=False)
    is_active = fields.BooleanField(default=False)
    is_admin = fields.BooleanField(default=False)
    date_joined = fields.DatetimeField(default=datetime.utcnow)
