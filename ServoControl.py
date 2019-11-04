#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Lordy
#
# Created:     01/11/2019
# Copyright:   (c) Lordy 2019
# Licence:     <your licence>
#-------------------------------------------------------------------------------

APPNAME = 'Servo Controller'
APPVERSION = '0.0.1'

# standard modules
import sys, os
from optparse import OptionParser
from functools import wraps

import wx
from wx import xrc

import serial

#local modules
#import util
import wxWrapper

class mainFrame(wxWrapper.Frame):
    _xrcName = "mainFrame"
    _tickTime = 500

    def __init__(self,xmlResource, parent = None):
        orig = xmlResource.LoadFrame(parent, self._xrcName)
        wxWrapper.Frame.__init__(self, orig)

        self.Fit()
        self.SetAutoLayout(True)
        #self.hookup('lblTblConStatus')
        #self.hookup('chkTblConStatus',self.OnToggleTblConnect,wx.EVT_CHECKBOX)
        #Window Menus
        #self.hookupMenu('mnuOpen', self.OnClickedOpen)
        wx.EVT_CLOSE(self, self.OnClose)

        self.reportError('')

        # wxGTK seems to need NewId() calls instead of default -1
        self.timerTick = wx.Timer(self, id=wx.NewId())
        wx.EVT_TIMER(self, self.timerTick.GetId(), self.OnTick)

        if not self.timerTick.Start(self._tickTime):
            print >>sys.stderr, 'Warning, could not create poll timer.'

    def hookup(self, id, handler = None, evtType = wx.EVT_BUTTON):
        """
        Attach a wxPython object to the specified
        xml id from the XRC file.  Optionally bind
        a command handler.
        """

        c = xrc.XRCCTRL(self, id)
        if c is None:
            raise NameError('Could not find XRC element id %s.' % id)

        setattr(self, id, c)
        if handler:
            self.Bind(evtType, handler, c)
        return c

    def hookupMenu(self, xmlid, handler):
        """ Bind to a menu event given an XRC element id. """
        wx.EVT_MENU(self, xrc.XRCID(xmlid), handler)

    def OnTick(self, evt=None):
        pass

    def OnClickedAbout(self, evt=None):
        from wx.lib.wordwrap import wordwrap
        info = wx.AboutDialogInfo()
        info.Name = APPNAME
        info.Version = APPVERSION
        info.Description = wordwrap( \
                "This program controls a set of"
                "Dynamixel XL-320 Servo Controllers"
                "Commands are accepted through the UI"
                "JSON commands can also be sent via UDP",
                200, wx.ClientDC(self))
        info.Developers = [ 'Shawn Lord']
        wx.AboutBox(info)




class ServoApp(wx.App):
    _guiFilename = "gui.xrc"

    def OnInit(self):
        self.res = xrc.XmlResource('gui.xrc')
        self.frame = mainFrame(self.res)
        self.SetTopWindow(self.frame)
        self.frame.Show()
        return True

    def getXmlResource(self):
        return self.res


if __name__ == '__main__':
    app = ServoApp(False)
    app.MainLoop()
    sys.exit(0)