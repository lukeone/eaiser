# -*- coding: utf-8 -*-
from prompt_toolkit.completion import Completer, Completion


class CommandCompleter(Completer):

    def __init__(self, context=None):
        self.context = context

    def get_completions(self, document, complete_event):
        topic = self.context.current
        word = document.get_word_before_cursor()

        if word.endswith(" "):
            pass

        for cmd, obj in topic.get_entrypoints().items():
            yield Completion(
                cmd,
                start_position=-len(word),
                style='bg:skyblue'
            )

