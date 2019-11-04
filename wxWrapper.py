"""
Alex Mekkering's little wrapper, taken from:
http://wiki.wxpython.org/index.cgi/UsingXmlResources

The purpose of these classes is to let you create your
own wrapper object to represent classes created by XRC.
"""

# vi:ts=4:noet:

import wx

class EvtHandler(wx.EvtHandler):
    def __init__(self, other):
        self.this = other.this
        self.thisown = 1
        del other
        self._setOORInfo(self)

# these are so cheap and similar i could probably
# accomplish this with a metaclass

class Frame(wx.Frame, EvtHandler):
    def __init__(self, other):
        EvtHandler.__init__(self, other)


class Dialog(wx.Dialog, EvtHandler):
    def __init__(self, other):
        EvtHandler.__init__(self, other)

