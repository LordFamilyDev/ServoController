"""
An implementation of a simple actor class.
"""

import sys
import threading
import Queue
from functools import wraps

__all__ = ['actormethod', 'ActorQuit', 'Actor']

def actormethod(mth):
    """
    Decorate a method such that it will be executed in the worker's
    thread.  The call will seem to return immediately, but the
    actual method will be invoked asynchronously whenever this
    Actor gets around to it.
    """
    @wraps(mth)
    def delayed(self, *args, **kwargs):
        self.queue.put((self, mth, args, kwargs))
    return delayed


class ActorQuit(StandardError):
    """
    Raise this exception when you want an actor thread to terminate.
    """
    def __init__(self):
        StandardError.__init__(self)

class Actor(threading.Thread):
    """
    Base class for specific Actor objects.  An Actor is an object
    with a work queue and its very own thread in which to execute
    items put in its work queue.

    See the async decorator for marking a method as asynchronous.

    Note that there is a potential for a reference leak if you don't
    explicitly kill the worker thread with the die() method; the
    run() method holds a reference to self, and unless you call
    die(), run() never terminates.

    Inspired by fraca7:
    http://fraca7.free.fr/blog/index.php?2005/04/17/
        15-design-patterns-part-v---actor
    """

    def __init__(self, *args, **kwargs):
        super(Actor, self).__init__(*args, **kwargs)
        self.setDaemon(True)

        self.queue = Queue.Queue()
        self.start()

    def fetchMethod(self, blocking=True):
        if blocking:
            return self.queue.get()
        else:
            return self.queue.get_nowait()

    def pumpMethod(self):
        """
        Fetch and invoke an actor method.  Simple enough here, but
        you may want to override it.
        """
        obj, mth, args, kwargs = self.fetchMethod()
        mth(obj, *args, **kwargs)

    def run(self):
        """
        This is the kernel of the actor.  The default implementation
        just pulls callables from the work queue and executes them
        in sequence.
        """
        while True:
            try:
                self.pumpMethod()
            except ActorQuit, ex:
                return
            except:
                # don't let other exceptions kill the thread
                import traceback
                traceback.print_exc(file=sys.stderr)
            finally:
                self.queue.task_done()

    @actormethod
    def die(self):
        raise ActorQuit


# vi:ts=4:sw=4:sts=4:nowrap:et:
