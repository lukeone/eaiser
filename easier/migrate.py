# -*- coding: utf-8 -*-
import db

from peewee_migrate import Router


def create():
    database = db.database
    database.connect()
    router = Router(database)

    # Create migration
    # router.create(name=BaseModel.sub_models())
    router.create(auto=db)

    # Run all unapplied migrations
    router.run()


if __name__ == "__main__":
    create()
    # print(BaseModel.sub_models())
