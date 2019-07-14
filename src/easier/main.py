# -*- coding: utf-8 -*-
import re

from .context import Context

pattern = re.compile(r"\\(?P<cmd>\w+) ?(?P<content>\S+)?")


def parse_command(text):
    """extract command and command content from input text

        such as:
            parse_command("/select_topic plan")
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

    inp = topic.session.prompt()
    if inp in ["exit", "quit"]:
        raise EOFError

    parsed = parse_command(inp)
    if parsed:
        cmd, val = parsed["cmd"].strip(), parsed["content"].strip()
        topic = context.current
        topic.execute_command(cmd, val)
    else:
        print("invalid input")
    return topic


def main():
    context = Context()
    while True:
        try:
            process_input(context)
        except KeyboardInterrupt:
            continue
        except EOFError:
            break
    print('GoodBye!')


if __name__ == "__main__":
    main()
