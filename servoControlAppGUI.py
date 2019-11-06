#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# generated by wxGlade 0.9.9pre on Tue Nov  5 22:20:19 2019
#

import wx
import wx.grid

# begin wxGlade: dependencies
# end wxGlade

# begin wxGlade: extracode
# end wxGlade


class servoControlFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: servoControlFrame.__init__
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL
        wx.Frame.__init__(self, *args, **kwds)
        self.SetSize((980, 585))
        self.SetTitle("Servo Control App")
        
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        
        self.panel_1 = wx.Panel(self, wx.ID_ANY)
        sizer_1.Add(self.panel_1, 1, wx.EXPAND, 0)
        
        sizer_5 = wx.BoxSizer(wx.HORIZONTAL)
        
        sizer_2 = wx.BoxSizer(wx.VERTICAL)
        sizer_5.Add(sizer_2, 1, wx.EXPAND, 0)
        
        sizer_3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_2.Add(sizer_3, 1, wx.EXPAND, 0)
        
        sizer_4 = wx.BoxSizer(wx.VERTICAL)
        sizer_3.Add(sizer_4, 0, 0, 0)
        
        self.tglbtnOpenPorts = wx.ToggleButton(self.panel_1, wx.ID_ANY, "Open Ports")
        sizer_4.Add(self.tglbtnOpenPorts, 0, wx.EXPAND, 0)
        
        self.btnFindServos = wx.Button(self.panel_1, wx.ID_ANY, "Refresh Servos")
        sizer_4.Add(self.btnFindServos, 0, wx.EXPAND, 0)
        
        self.btnEnableServos = wx.Button(self.panel_1, wx.ID_ANY, "Enable Servos")
        sizer_4.Add(self.btnEnableServos, 0, wx.EXPAND, 0)
        
        self.btnResetServos = wx.Button(self.panel_1, wx.ID_ANY, "Reset Servos")
        sizer_4.Add(self.btnResetServos, 0, wx.EXPAND, 0)
        
        self.servoGrid = wx.grid.Grid(self.panel_1, wx.ID_ANY, size=(1, 1))
        self.servoGrid.CreateGrid(17, 10)
        self.servoGrid.SetRowLabelSize(0)
        self.servoGrid.EnableEditing(0)
        self.servoGrid.SetSelectionMode(wx.grid.Grid.SelectRows)
        self.servoGrid.SetColLabelValue(0, "Servo")
        self.servoGrid.SetColSize(0, 87)
        self.servoGrid.SetColLabelValue(1, "ID")
        self.servoGrid.SetColSize(1, 36)
        self.servoGrid.SetColLabelValue(2, "Status")
        self.servoGrid.SetColSize(2, 90)
        self.servoGrid.SetColLabelValue(3, "Position")
        self.servoGrid.SetColSize(3, 59)
        self.servoGrid.SetColLabelValue(4, "Start")
        self.servoGrid.SetColSize(4, 53)
        self.servoGrid.SetColLabelValue(5, "End")
        self.servoGrid.SetColSize(5, 50)
        self.servoGrid.SetColLabelValue(6, "Speed")
        self.servoGrid.SetColSize(6, 49)
        self.servoGrid.SetColLabelValue(7, "Torque")
        self.servoGrid.SetColSize(7, 49)
        self.servoGrid.SetColLabelValue(8, "Voltage")
        self.servoGrid.SetColSize(8, 49)
        self.servoGrid.SetColLabelValue(9, "Temp")
        self.servoGrid.SetColSize(9, 49)
        sizer_3.Add(self.servoGrid, 1, wx.EXPAND, 0)
        
        grid_sizer_1 = wx.FlexGridSizer(9, 2, 1, 1)
        sizer_3.Add(grid_sizer_1, 0, wx.ALL | wx.EXPAND, 1)
        
        static_text_4 = wx.StaticText(self.panel_1, wx.ID_ANY, "Servo Name")
        grid_sizer_1.Add(static_text_4, 0, 0, 0)
        
        self.txtServoName = wx.TextCtrl(self.panel_1, wx.ID_ANY, "")
        grid_sizer_1.Add(self.txtServoName, 0, 0, 0)
        
        static_text_1 = wx.StaticText(self.panel_1, wx.ID_ANY, "Servo ID:")
        grid_sizer_1.Add(static_text_1, 0, 0, 0)
        
        self.txtServoId = wx.TextCtrl(self.panel_1, wx.ID_ANY, "")
        grid_sizer_1.Add(self.txtServoId, 0, 0, 0)
        
        static_line_3 = wx.StaticLine(self.panel_1, wx.ID_ANY)
        grid_sizer_1.Add(static_line_3, 0, wx.EXPAND, 0)
        
        static_line_4 = wx.StaticLine(self.panel_1, wx.ID_ANY)
        grid_sizer_1.Add(static_line_4, 0, wx.EXPAND, 0)
        
        static_text_2 = wx.StaticText(self.panel_1, wx.ID_ANY, "Position:")
        grid_sizer_1.Add(static_text_2, 0, 0, 0)
        
        self.txtServoPosition = wx.TextCtrl(self.panel_1, wx.ID_ANY, "")
        grid_sizer_1.Add(self.txtServoPosition, 0, 0, 0)
        
        static_text_3 = wx.StaticText(self.panel_1, wx.ID_ANY, "Speed:")
        grid_sizer_1.Add(static_text_3, 0, 0, 0)
        
        self.txtServoSpeed = wx.TextCtrl(self.panel_1, wx.ID_ANY, "")
        grid_sizer_1.Add(self.txtServoSpeed, 0, 0, 0)
        
        grid_sizer_1.Add((0, 0), 0, 0, 0)
        
        self.btnGo = wx.Button(self.panel_1, wx.ID_ANY, "GO")
        grid_sizer_1.Add(self.btnGo, 0, wx.ALIGN_CENTER, 0)
        
        static_line_1 = wx.StaticLine(self.panel_1, wx.ID_ANY)
        grid_sizer_1.Add(static_line_1, 0, wx.EXPAND, 0)
        
        static_line_2 = wx.StaticLine(self.panel_1, wx.ID_ANY)
        grid_sizer_1.Add(static_line_2, 0, wx.EXPAND, 0)
        
        self.btnStart = wx.Button(self.panel_1, wx.ID_ANY, "Go Start")
        grid_sizer_1.Add(self.btnStart, 0, wx.ALIGN_CENTER, 0)
        
        self.btnEnd = wx.Button(self.panel_1, wx.ID_ANY, "Go End")
        grid_sizer_1.Add(self.btnEnd, 0, wx.ALIGN_CENTER, 0)
        
        self.btnEnableServo = wx.Button(self.panel_1, wx.ID_ANY, "Enable")
        grid_sizer_1.Add(self.btnEnableServo, 0, wx.ALIGN_CENTER, 0)
        
        self.btnResetServo = wx.Button(self.panel_1, wx.ID_ANY, "Reset")
        grid_sizer_1.Add(self.btnResetServo, 0, wx.ALIGN_CENTER, 0)
        
        self.txtLog = wx.TextCtrl(self.panel_1, wx.ID_ANY, "", style=wx.HSCROLL | wx.TE_DONTWRAP | wx.TE_MULTILINE | wx.TE_READONLY)
        self.txtLog.SetMinSize((-1, 200))
        sizer_2.Add(self.txtLog, 0, wx.EXPAND, 0)
        
        self.panel_1.SetSizer(sizer_5)
        
        self.SetSizer(sizer_1)
        
        self.Layout()

        self.Bind(wx.EVT_TOGGLEBUTTON, self.onTglBtnOpenPorts, self.tglbtnOpenPorts)
        self.Bind(wx.EVT_BUTTON, self.onClickFindServos, self.btnFindServos)
        self.Bind(wx.EVT_BUTTON, self.onClickEnableServos, self.btnEnableServos)
        self.Bind(wx.EVT_BUTTON, self.onClickResetServos, self.btnResetServos)
        self.Bind(wx.grid.EVT_GRID_CMD_SELECT_CELL, self.onServoSelect, self.servoGrid)
        self.Bind(wx.EVT_BUTTON, self.onBtnGo, self.btnGo)
        self.Bind(wx.EVT_BUTTON, self.onBtnGoStart, self.btnStart)
        self.Bind(wx.EVT_BUTTON, self.onBtnGoEnd, self.btnEnd)
        self.Bind(wx.EVT_CLOSE, self.onClose, self)
        # end wxGlade

    def onTglBtnOpenPorts(self, event):  # wxGlade: servoControlFrame.<event_handler>
        print("Event handler 'onTglBtnOpenPorts' not implemented!")
        event.Skip()

    def onClickFindServos(self, event):  # wxGlade: servoControlFrame.<event_handler>
        print("Event handler 'onClickFindServos' not implemented!")
        event.Skip()

    def onClickEnableServos(self, event):  # wxGlade: servoControlFrame.<event_handler>
        print("Event handler 'onClickEnableServos' not implemented!")
        event.Skip()

    def onClickResetServos(self, event):  # wxGlade: servoControlFrame.<event_handler>
        print("Event handler 'onClickResetServos' not implemented!")
        event.Skip()

    def onServoSelect(self, event):  # wxGlade: servoControlFrame.<event_handler>
        print("Event handler 'onServoSelect' not implemented!")
        event.Skip()

    def onBtnGo(self, event):  # wxGlade: servoControlFrame.<event_handler>
        print("Event handler 'onBtnGo' not implemented!")
        event.Skip()

    def onBtnGoStart(self, event):  # wxGlade: servoControlFrame.<event_handler>
        print("Event handler 'onBtnGoStart' not implemented!")
        event.Skip()

    def onBtnGoEnd(self, event):  # wxGlade: servoControlFrame.<event_handler>
        print("Event handler 'onBtnGoEnd' not implemented!")
        event.Skip()

    def onClose(self, event):  # wxGlade: servoControlFrame.<event_handler>
        print("Event handler 'onClose' not implemented!")
        event.Skip()

# end of class servoControlFrame

class servoControlApp(wx.App):
    def OnInit(self):
        self.servoControlFrame = servoControlFrame(None, wx.ID_ANY, "")
        self.SetTopWindow(self.servoControlFrame)
        self.servoControlFrame.Show()
        return True

# end of class servoControlApp

if __name__ == "__main__":
    servoControlApp = servoControlApp(0)
    servoControlApp.MainLoop()
