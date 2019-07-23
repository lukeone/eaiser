# -*- coding: utf-8 -*-
import tableprint

from .context import Context
from .completer import CommandCompleter
from .util import parse_command


def process_input(context):
    """handle user's input, and handle one input every time
        so you might put it in a loop, such as:
            while True:
                process_input(context)

    :param context: context
    :return: next topic
    """

    topic = context.current

    context.input_start()
    inp = topic.session.prompt(complete_while_typing=True,
                               completer=CommandCompleter(context),
                               refresh_interval=1,
                               complete_in_thread=True).strip()
    context.input_over()

    parsed = parse_command(inp)
    if parsed:
        cmd, val = parsed["cmd"].strip(), (parsed["content"] or "").strip()
        topic.execute_command(cmd, val)
    return topic


def main():

    tableprint.banner("Easier Life! Easier Work!")

    context = Context()
    while True:
        try:
            process_input(context)
        except KeyboardInterrupt:
            continue
        except EOFError:
            break
    print('GoodBye!')
