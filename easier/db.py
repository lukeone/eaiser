# -*- coding: utf-8 -*-
import os

import peewee as pw

CUR_DIR = os.path.abspath(os.path.dirname(__file__))

database = pw.SqliteDatabase(os.path.join(CUR_DIR, "storage", "easier.db"))


class BaseModel(pw.Model):

    class Meta:
        database = database

    version = pw.IntegerField(default=0)

    @classmethod
    def sub_models(cls):
        return {
            sub.__name__: sub for sub in cls.__subclasses__()
        }

    @classmethod
    def check_schema_migration(cls):
        to_created = filter(lambda obj: not obj.table_exists(),
                            cls.sub_models().values())
        database.create_tables(to_created)


class SystemParameter(BaseModel):

    key = pw.CharField(index=True, unique=True, max_length=128)
    value = pw.CharField(max_length=1024)
