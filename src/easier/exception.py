# -*- coding: utf-8 -*-


class CommandNotFound(Exception):

    def __init__(self, message="", command=""):
        if not message:
            message = "Command Not Found"
        if command:
            message = "{}: \\{}".format(message, command)

        super(CommandNotFound, self).__init__(message)