# -*- coding: utf-8 -*-

from .core import Topic


class Plan(Topic):

    _name = "plan"
    _description = "plan manager"

    def add_journal(self):
        pass

    def remove_journal(self):
        pass