# -*- coding: utf-8 -*-

from abc import ABCMeta
from prompt_toolkit import PromptSession
from ..exception import CommandNotFound


def entrypoint(method):
    """Decorate one method as a command entrypoint. like:

            @entrypoint
            def help(self):
                pass

    :param method: decorated method of topic class
    :return: method
    """
    method.__entrypoint = True
    return method


class TopicMeta(ABCMeta):

    # all topic class, eg: {"": DefaultTopic, "other": OtherTopic}
    _topic_classes = {}
    # topic entrypoint per topic, eg: {'': {'select_topic': <function Topic.select_topic at 0x109d9bc80>}}
    _topic_entrypoints = {}

    def __init__(self, name, bases, members):
        super(TopicMeta, self).__init__(name, bases, members)
        mcls = self.__class__

        mcls._topic_classes[self._name] = self
        mcls._topic_entrypoints[self._name] = {}

        for attr, method in members.items():
            if not getattr(method, "__entrypoint", False):
                continue
            mcls._topic_entrypoints[self._name][attr] = method

        for base in bases:
            if not isinstance(base, mcls):
                continue
            mcls._topic_entrypoints[self._name].update(mcls._topic_entrypoints[base._name])

    @classmethod
    def create_topic(mcls, name, context):
        """create a topic instance

        :param mcls: TopicMeta
        :param name: topic name
        :param context: `easier.Context` object
        :return: topic object
        """
        assert name in mcls._topic_classes
        topic = mcls._topic_classes[name](context)
        return topic

    @classmethod
    def get_entrypoint(mcls, name, cmd):
        """return entrypoint function object, if not exist, return None
        
        :param name: topic name
        :param cmd: entrypoint function name
        :return: function object
        """
        return mcls._topic_entrypoints.get(name, {}).get(cmd, None)


class Topic(object, metaclass=TopicMeta):

    _name = None

    def __init__(self, context):
        self.context = context
        self.session = PromptSession("%s> " % self.name)

    def release(self):
        """relase resource and reference
        """
        self.context = None
        self.session = None

    def execute_command(self, cmd, content):
        """determine entrypoint funcion, and call it.
        
        :param cmd: command name, also is entrypoint function name
        :param content: command content, also is entrypoint function arguments
        """
        entrypoint = TopicMeta.get_entrypoint(self.name, cmd)
        if not entrypoint:
            raise CommandNotFound(command=cmd)
        res = entrypoint(self, content)
        return res

    @property
    def name(self):
        """the topic's name, it's a class attribute
        """
        return self._name

    @entrypoint
    def select_topic(self, name):
        """switch topic

        :param name: topic name
        :return:
        """
        topic = self.context.get_topic(name)
        self.context.set_current(topic)


class DefaultTopic(Topic):

    _name = ""


if __name__ == "__main__":
    t1 = DefaultTopic(x=1)
    print(t1.name)
