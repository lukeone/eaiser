# -*- coding: utf-8 -*-
import os
import importlib

from .core import (Topic, TopicMeta, DefaultTopic)
from ..db import BaseModel

__all__ = (Topic, TopicMeta, DefaultTopic)


def load_topic_module():
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    for par, dirs, files in os.walk(cur_dir):
        for pyfile in files:
            if not pyfile.endswith(".py") or pyfile in ["__init__.py"]:
                continue
            rel_name = os.path.relpath(os.path.join(par, pyfile), cur_dir)
            module_name = "." + rel_name.rstrip(".py").replace(os.path.sep, ".")
            importlib.import_module(module_name, package="easier.topic")


load_topic_module()


def check_schema_migration():
    BaseModel.check_schema_migration()
