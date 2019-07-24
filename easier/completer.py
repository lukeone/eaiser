# -*- coding: utf-8 -*-
from prompt_toolkit.completion import Completer, Completion
from .util import parse_command


class CommandCompleter(Completer):
    """
    auto-completer
    """

    def __init__(self, context=None):
        self.context = context

    def get_completions(self, document, complete_event):
        topic = self.context.current
        word = document.get_word_before_cursor()
        self.context.inputting = document.text

        if word == document.text:                       # suppose user is typing command
            for cmd, obj in topic.get_entrypoints().items():
                if word and not cmd.startswith(word):
                    continue
                yield Completion(
                    cmd,
                    start_position=-len(word),
                    style='bg:skyblue'
                )
        else:                                           # typing command content
            """
            custome auto complete behavior for command parameter
            use it such as:

                def complete_func_name(self, content):
                    "return list or iterable Complettion"
                    pass

                @entrypoint(complete="complete_func_name")
                def the_func_name(self, content)
                    pass
            """

            cmd_info = parse_command(document.text) or {}
            entrypoint = topic.get_entrypoint(cmd_info.get("cmd", ""))
            if not entrypoint or not entrypoint.complete:
                return
            complete_func = getattr(topic, entrypoint.complete)
            for completion in complete_func(cmd_info["content"]):
                yield completion
