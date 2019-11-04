"""
Miscellanous utility functions I don't know what else to do with.
"""

from __future__ import generators

import sys
import serial    # http://pyserial.sf.net
from functools import wraps

"""
class Struct(object):
    "" "
    An object that has attributes built from the dictionary given in
    constructor. So ss=Struct(a=1, b='b') will satisfy assert ss.a
    == 1 and assert ss.b == 'b'.
    "" "
    def __init__(self, *args, **kwargs):
        "" "
        We can either initialize from another Struct
        or from keyword args.
        "" "
        if len(args) == 1 and isinstance(args[0], Struct):
            self.__dict__.update(args[0].__dict__)
        else:
            self.__dict__.update(kwargs)
    # todo: implement this in a prettier way
    def asDict(self):
        return self.__dict__
    def __getitem__(self, key):
        return getattr(self, key)
    def __setitem__(self, key, val):
        setattr(self, key, val)
    def __delitem__(self, key):
        delattr(self, key)
    def iteritems(self):
        return self.__dict__.iteritems()
"""

def bound(v, vMin, vMax):
    """
    Return the closest realizable value to v given constraints
    vMin and vMax.
    """
    return max(min(v, vMax), vMin)

def enumSerialPorts(howmany = 30):
    """
    Generate a series of possible serial port names.
    These ports are not guaranteed to actually exist on the system.
    Also, they are raw names, so you'll get \\.\COM10 on Windows.
    """
    s = serial.Serial()
    for i in range(howmany):
        yield s.makeDeviceName(i)


def getDefaultSerialPort():
    """
    Return a sensible default serial port (e.g. COM1 or /dev/ttyS0).
    """
    s = serial.Serial()
    return s.makeDeviceName(0)


def sanitizePort(name):
    """
    Convert a raw device filename to a form suitable for showing to
    the user.  E.g., on Windows, COM ports above COM9 are prefixed
    with \\.\ for some reason.

    On other platforms, this is a no-op.

    This is an idempotent operation.
    """

    if sys.platform == 'win32':
        # deal with windows weirdness
        if name.startswith('\\\\.\\'):
            return str(name[4:])

    return str(name)


def unsanitizePort(name):
    """
    Convert a friendly serial port name into the actual device
    filename.  E.g., on Windows, COM ports above COM9 are prefixed
    with \\.\ for some reason.

    On other platforms, this is a no-op.

    This is an idempotent operation.
    """
    if sys.platform == 'win32':
        # deal with windows weirdness
        # COMx passes through, but
        # COMxx -> \\.\COMxx
        if len(name) > 4 and not name.startswith('\\\\.\\'): 
            return '\\\\.\\' + str(name)

    return str(name)


def retryify(func, times, exceptions):
    """
    Return a new callable wrapping 'func' which will check for the
    specified exceptions and re-call the function up to the specified
    number of times.  If an exception not specified occurs, it will
    be re-raised up to the caller.  If the maximum number of retries
    has elapsed, even exceptions specified by the caller will be be
    re-raised.

    Caught exceptions are compared with those specified via the user
    similarly to a normal exception handler; e.g., if the exception
    caught is derived from a listed exception, this will count as a
    match.

    Arguments:
    func -- callable to wrap
    times -- number of times to re-call func()
    exceptions -- tuple of exceptions which are retriable; if not a
    tuple it will be coerced into one.
    """
    exceptions = tuple(exceptions)

    # build a little helper function to wrap the function. 
    # it will be bound to our args via lexical closure.
    @wraps(func)
    def f(*args, **kwargs):
        for i in xrange(times-1):
            try:
                return func(*args, **kwargs)
            except:
                # now check if this exception is in the list
                exc, val = sys.exc_info()[:2]
                if not issubclass(exc, exceptions):
                    raise exc, val, sys.exc_info()[2]

            # if we got here, we already tried as much as we could;
            # one last try without exception protection
            return func(*args)

    # f.__doc__ == func.__doc__
    # f.func_doc maybe?

    return f

# vi:ts=4:sw=4:sts=4:nowrap:et:
