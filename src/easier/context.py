# -*- coding: utf-8 -*-
from .topic import DefaultTopic, TopicMeta


class Context(object):
    """a context used to represent current session and save other
        data in this current session.
    """

    def __init__(self):
        self.current = DefaultTopic(self)

        # save history topic, order by add time, and without duplicate
        self.queue = []
        # define the max size of queue
        self.queue_max_size = 5

    def set_current(self, topic):
        """
        set current topic

        :param topic: the instance of `topic.Topic`
        :return:
        """

        if self.current == topic:
            return
        if self.current in self.queue:
            self.queue.remove(self.current)
        self.queue.append(self.current)
        self.current = topic
        self._check_queue_size()

    def _check_queue_size(self):
        """
        check weather the size of queue is exceed the limit.

        if exceeded, then pop the head topic

        :return:
        """
        while len(self.queue) > self.queue_max_size:
            to_del = self.queue.pop(0)
            to_del.release()

    def get_topic(self, name):
        """
        return the topic instance by name

        if the topic exist in context already, then return it.
        but if not exist, new one.

        :param name: topic name
        :return: topic instance
        """
        if self.current.name == name:
            return self.current

        for topic in self.queue:
            if topic.name != name:
                continue
            return topic
        topic = TopicMeta.create_topic(name, self)
        return topic


