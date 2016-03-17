#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'dong'


try:
    import psyco
    psyco.full()
except:
    pass

import peewee
import datetime
from models.base import BaseModel


class User(BaseModel):
    user_id = peewee.CharField(index=True, max_length=30)
    username = peewee.CharField()
    password = peewee.CharField()
    mobile = peewee.CharField(index=True, max_length=20)
    created_at = peewee.DateField(default=datetime.datetime.now)
    updated_at = peewee.DateField(default=datetime.datetime.now)

    class Meta:
        db_table = 'user'
        order_by = ('-updated_at',)