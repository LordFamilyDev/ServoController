"""
An ultra simple publisher/subscriber system, implemented in terms of
a MixIn class.  When combined with decorators, you can have message
handlers occur in specified threads, or other gee-whiz tricks.
"""

__all__ = ['PublisherMixIn', 'Message']

class Message(object):
    """
    Suggested base class for published messages intended to allow
    for automatic "updates" to message classes.  Messages can be any
    class type, however, because they employ duck typing.  There are
    no inheritance checks for this class.
    """
    pass

class PublisherMixIn(object):
    """
    This class implements part of a very simple publisher/subscriber
    system.  It is indented to be used as a mixin via multiple
    inheritance.
    """
    def __init__(self):
        # dict of lists indexed by event class
        self.subMap = {}

    def subscribe(self, eventClass, subscriber):
        """
        eventClass is a type representing the event the subscriber
        is interested in.
        subscriber is a callable which takes an instance of
        eventClass as its sole argument.
        """
        if eventClass in self.subMap:
            self.subMap[eventClass].append(subscriber)
        else:
            self.subMap[eventClass] = [subscriber]

    def unsubscribe(self, eventClass, subscriber):
        l = self.subMap.get(eventClass, [])
        if subscriber in l:
            l.remove(subscriber)

    def publish(self, eventInst):
        for eventClass, clients in self.subMap.iteritems():
            if isinstance(eventInst, eventClass):
                for client in clients:
                    client(eventInst)


# vi:ts=4:sw=4:sts=4:nowrap:et:
