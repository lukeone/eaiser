# -*- coding: utf-8 -*-

import os
import tableprint

from abc import ABCMeta
from prompt_toolkit import PromptSession, print_formatted_text, HTML
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.history import FileHistory
from prompt_toolkit.completion import Completion


def entrypoint(alias=None, doc="", complete=None):
    """Decorate one method as a command entrypoint. like:

            @entrypoint()
            def help(self):
                pass

    :param alias: give one entrypoint multi command name
    :param doc: the command description
    :return: method
    """
    alias = [] if alias is None else alias

    def wrap(method):
        """
        :param method: decorated method of topic class
        :return:
        """
        name = method.__name__
        if name not in alias:
            alias.insert(0, name)

        method._entrypoint = True
        method._flags = alias
        method._doc = doc
        method.complete = complete
        return method
    return wrap


class TopicMeta(ABCMeta):

    # all topic class
    # eg: {"": DefaultTopic, "other": OtherTopic}
    topic_classes = {}

    # topic entrypoint per topic
    # eg: {'': {'select_topic': <function Topic.select_topic at 0x109d9bc80>}}
    topic_entrypoints = {}

    def __init__(self, name, bases, members):
        super(TopicMeta, self).__init__(name, bases, members)
        mcls = self.__class__

        mcls.topic_classes[self._name] = self
        mcls.topic_entrypoints[self._name] = {}

        for attr, method in members.items():
            if not getattr(method, "_entrypoint", False):
                continue
            mcls.topic_entrypoints[self._name].update(dict.fromkeys(method._flags, method))

        for base in bases:
            if not isinstance(base, mcls):
                continue
            mcls.topic_entrypoints[self._name].update(mcls.topic_entrypoints[base._name])

    @classmethod
    def create_topic(mcls, name, context):
        """create a topic instance

        :param mcls: TopicMeta
        :param name: topic name
        :param context: `easier.Context` object
        :return: topic object
        """
        if name not in mcls.topic_classes:
            return None
        topic = mcls.topic_classes[name](context)
        return topic


class Topic(object, metaclass=TopicMeta):

    _name = None

    def __init__(self, context):
        self.context = context
        self.session = PromptSession("%s> " % self.name,
                                     history=FileHistory(self._history_filename()),
                                     auto_suggest=AutoSuggestFromHistory())

    def release(self):
        """relase resource and reference
        """
        self.context = None
        self.session = None

    def _history_filename(self):
        filename = '.history/{}'.format(self._name)
        dirname = os.path.dirname(filename)
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        return filename

    def get_entrypoint(self, cmd):
        """find entrypoint by command name

        :param cmd: command
        :return: entrypoint function object
        """
        return TopicMeta.topic_entrypoints.get(self._name, {}).get(cmd, None)

    def get_entrypoints(self):
        """return all entrypoint in this topic

        :return: all entrypoint data
        """
        return TopicMeta.topic_entrypoints.get(self._name, {})

    @staticmethod
    def _get_topics():
        """return all topic name
        """
        return {name: obj for name, obj in TopicMeta.topic_classes.items() if bool(name)}

    def execute_command(self, cmd, content):
        """determine entrypoint funcion, and call it.

        :param cmd: command name, also is entrypoint function name
        :param content: command content, also is entrypoint function arguments
        """
        func = self.get_entrypoint(cmd)
        if not func:
            self.command_not_found(cmd)
            return

        args = [content] if content else []

        try:
            func(self, *args)
        except TypeError:
            self.lack_command_options(cmd)

    @staticmethod
    def command_not_found(cmd):
        print_formatted_text(HTML('<ansired>invalid command, type "help" for more information</ansired>'))

    @staticmethod
    def lack_command_options(cmd):
        print_formatted_text(HTML('<ansired>command option error</ansired>'))

    @staticmethod
    def topic_not_found(name):
        print_formatted_text(
            HTML('<ansired>topic "{}" not found, type "list_topics" for more information</ansired>'.format(name)))

    @property
    def name(self):
        """the topic's name, it's a class attribute
        """
        return self._name

    def _topic_completions(self, content):
        """ auto complete when typing topic

        :param content: command content
        :return:
        """

        commands = self._get_topics()
        for name, _ in commands.items():
            yield Completion(
                name,
                start_position=-len(content),
                style='bg:seagreen'
            )

    @entrypoint(
        doc="change topic, eg: > 'select_topic plan'",
        complete="_topic_completions"
    )
    def select_topic(self, name):
        """change topic

        :param name: topic name
        :return:
        """
        topic = self.context.get_topic(name)
        if not topic:
            self.topic_not_found(name)
            return
        self.context.set_current(topic)

    @entrypoint(doc="show all topic")
    def list_topics(self):
        """show topic list
        """
        rows = []
        header = ("topic", "description")
        mx_topic_size = len(header[0])
        mx_desc_size = len(header[1])

        for topic, tcls in self._get_topics().items():
            mx_topic_size = max(mx_topic_size, len(topic))
            mx_desc_size = max(mx_desc_size, len(tcls._description))
            rows.append((topic, tcls._description))

        tableprint.table(rows, ("topic", "description"), width=(mx_topic_size + 5, mx_desc_size + 5))

    @entrypoint(alias=["quit"], doc="quit program")
    def exit(self, *args):
        raise EOFError

    @entrypoint(doc="clear screen")
    def clear(self):
        """clear screen
        """
        os.system("clear")

    @entrypoint(doc="show all available commands")
    def help(self):
        rows = []
        header = ("command", "description")
        mx_cmd_size = len(header[0])
        mx_desc_size = len(header[1])

        for name, obj in self.get_entrypoints().items():
            mx_cmd_size = max(mx_cmd_size, len(name))
            mx_desc_size = max(mx_desc_size, len(obj._doc))
            rows.append((name, obj._doc))

        rows.sort(key=lambda k: "z" if k[0] in ["exit", "quit", "help", "clear"] else k[0])
        tableprint.table(rows, header, width=(mx_cmd_size + 5, mx_desc_size + 5))


class DefaultTopic(Topic):

    _name = "default"
    _description = "default topic"
