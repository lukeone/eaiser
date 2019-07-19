# -*- coding: utf-8 -*-
import re
import tableprint

from .context import Context
from .completer import CommandCompleter

pattern = re.compile(r"(?P<cmd>\w+) ?(?P<content>.*)?")


def parse_command(text):
    """extract command and command content from input text

        such as:
            parse_command("select_topic plan")
            >> {"command": "select_topic", "content": "plan"}

    :param text: the input text
    :return:
    """
    match = pattern.match(text)
    if match:
        return match.groupdict()
    return None


def process_input(context):
    """handle user's input, and handle one input every time
        so you might put it in a loop, such as:
            while True:
                process_input(context)

    :param context: context
    :return: next topic
    """

    topic = context.current

    inp = topic.session.prompt(complete_while_typing=True,
                               completer=CommandCompleter(context),
                               complete_in_thread=True).strip()
    if not inp:
        return

    parsed = parse_command(inp)
    if parsed:
        cmd, val = parsed["cmd"].strip(), (parsed["content"] or "").strip()
        topic.execute_command(cmd, val)
    else:
        topic.command_not_found(inp)
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
