import wx
import gettext
import threading
import queue

from dynamixel_sdk import robotis_def
from servoControlAppGUI import servoControlFrame
from Servo import Servo
from UDPCommandListener import UDPServerThread, UDPDataHandler

import ServoConfig

NUM_RETRIES = 3

class mainFrame(servoControlFrame):
    __gridColName = 0
    __gridColID = 1
    __gridColStatus = 2
    __gridColPosition = 3
    __gridColStart = 4
    __gridColEnd = 5
    __gridColSpeed = 6
    __gridColTorque = 7
    __gridColVoltage = 8
    __gridColTemp = 9

    def __init__(self,*args,**kwds):
        servoControlFrame.__init__(self,*args,**kwds)
        self.servoCtrl = Servo()
        self.initGrid()
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER,self.onTick,self.timer)
        self.timer.Start(100)

        self.servoUpdateRow = 0

        self.cmdQ = queue.Queue()
        self.server = UDPServerThread(ServoConfig.UDPPort, UDPDataHandler, queue=self.cmdQ)
        self.server_thread = threading.Thread(target=self.server.serve_forever)
        self.server_thread.daemon = True
        self.server_thread.start()


    def initGrid(self):
        row = 0
        servoList = self.servoCtrl.servoList
        for servo in servoList:
            self.servoCtrl.servoList[servo]['Row']=row
            self.servoGrid.SetCellValue(row,self.__gridColName,servo)
            self.servoGrid.SetCellValue(row,self.__gridColID,str(servoList[servo]['ID']))
            self.servoGrid.SetCellValue(row,self.__gridColStatus,str("Port Closed"))
            self.servoGrid.SetCellValue(row,self.__gridColPosition,"")
            self.servoGrid.SetCellValue(row,self.__gridColStart,str(servoList[servo]['StartPos']))
            self.servoGrid.SetCellValue(row,self.__gridColEnd,str(servoList[servo]['EndPos']))
            self.servoGrid.SetCellValue(row,self.__gridColSpeed,str(servoList[servo]['Speed']))
            row += 1

    def onTick(self, event):
        if not self.cmdQ.empty():
            try:
                cmd = self.cmdQ.get_nowait()
                self.cmdQ.task_done()
            except:
                pass
            self.parseCmd(cmd)

        self.updateServo(self.servoGrid.GetCellValue(self.servoUpdateRow,self.__gridColName))
        self.servoUpdateRow += 1
        if(self.servoUpdateRow >= len(self.servoCtrl.servoList)): self.servoUpdateRow = 0
        pass
    
    def parseCmd(self,cmd):
        print("Got:" + str(cmd))
        cmds = cmd.decode("utf-8").split("\n")
        for c in cmds:
            c = c.strip(" 	{}")
            args = c.split(":")
            if(len(args) < 2): 
                print("no commands found")
                return
            servo = args[0]
            if not servo in self.servoCtrl.servoList:
                print ("servo %s not found"%(servo))
                return
            
            if(len(args) > 2):
                speed = args[2]
            else:
                speed = self.servoCtrl.servoList[servo]['Speed']
            
            if args[1] in self.servoCtrl.servoList[servo]['Positions']:
                position = self.servoCtrl.servoList[servo]['Positions'][args[1]]
            else:
                try:
                    position = int(args[1])
                except:
                    print("Could not parse Position")
                    return
            print("Setting %s to Speed: %u, and Pos %u"%(servo,speed,position))
            self.servoCtrl.setSpeed(servo,speed)
            self.servoCtrl.setPosition(servo,position)




    def onTglBtnOpenPorts(self, event):  # wxGlade: servoControlFrame.<event_handler>
        if(not self.tglbtnOpenPorts.GetValue()):
            print("Closing Com Ports")
            self.servoCtrl.closeServoPort()
            self.tglbtnOpenPorts.Label = "Open Ports"
        else:
            print("Opening Com Ports")
            self.servoCtrl.openServoPort()
            self.updateServos()
            self.tglbtnOpenPorts.Label = "Close Ports"

    def onClickFindServos(self, event):  # wxGlade: servoControlFrame.<event_handler>
        self.updateServos()
        event.Skip()

    def updateServos(self):
        s = self.servoCtrl
        if( not self.servoCtrl.isConnected()):
            for servo in s.servoList:
                self.servoGrid.SetCellValue(s.servoList[servo]['Row'],self.__gridColStatus,"COMM CLOSED")
            return
        for servo in s.servoList:
            print("Pinging Servo "+servo)
            (model,result, error) = s.ping(servo)
            if(result == robotis_def.COMM_SUCCESS):
                self.servoGrid.SetCellValue(s.servoList[servo]['Row'],self.__gridColStatus,s.getStatus(servo))
                self.servoGrid.SetCellValue(s.servoList[servo]['Row'],self.__gridColPosition,str(s.getPosition(servo)))
                self.servoGrid.SetCellValue(s.servoList[servo]['Row'],self.__gridColTorque,str(s.getTorque(servo)))
                self.servoGrid.SetCellValue(s.servoList[servo]['Row'],self.__gridColVoltage,str(s.getVoltage(servo)))
                self.servoGrid.SetCellValue(s.servoList[servo]['Row'],self.__gridColTemp,str(s.getTemp(servo)))

            else:
                self.servoGrid.SetCellValue(s.servoList[servo]['Row'],self.__gridColStatus,"Not Responding")

    def updateServo(self,servo):
        s = self.servoCtrl
        if( not self.servoCtrl.isConnected()):
            for servo in s.servoList:
                self.servoGrid.SetCellValue(s.servoList[servo]['Row'],self.__gridColStatus,"COMM CLOSED")
            return
        if servo in s.servoList:
            print("Pinging Servo "+servo)
            (model,result, error) = s.ping(servo)
            if(result == robotis_def.COMM_SUCCESS):
                self.servoGrid.SetCellValue(s.servoList[servo]['Row'],self.__gridColStatus,s.getStatus(servo))
                self.servoGrid.SetCellValue(s.servoList[servo]['Row'],self.__gridColPosition,str(s.getPosition(servo)))
                self.servoGrid.SetCellValue(s.servoList[servo]['Row'],self.__gridColTorque,str(s.getTorque(servo)))
                self.servoGrid.SetCellValue(s.servoList[servo]['Row'],self.__gridColVoltage,str(s.getVoltage(servo)))
                self.servoGrid.SetCellValue(s.servoList[servo]['Row'],self.__gridColTemp,str(s.getTemp(servo)))
            else:
                self.servoGrid.SetCellValue(s.servoList[servo]['Row'],self.__gridColStatus,"Not Responding")

    def onClickEnableServos(self, event):  # wxGlade: servoControlFrame.<event_handler>
        self.enableServos()

    def enableServos(self):
        print("Enabling Servo's")
        s = self.servoCtrl
        for servo in s.servoList:
            result, error = s.enableServo(servo )
        self.updateServos()


    def onClickResetServos(self, event):  # wxGlade: servoControlFrame.<event_handler>
        print("Event handler 'onClickResetServos' not implemented!")
        event.Skip()

    def onServoSelect(self, event):  # wxGlade: servoControlFrame.<event_handler>
        row = event.GetRow()
        self.txtServoName.SetValue(self.servoGrid.GetCellValue(row,self.__gridColName))
        self.txtServoId.SetValue(self.servoGrid.GetCellValue(row,self.__gridColID))
        self.txtServoPosition.SetValue(self.servoGrid.GetCellValue(row,self.__gridColPosition))
        self.txtServoSpeed.SetValue(self.servoGrid.GetCellValue(row,self.__gridColSpeed))

    def onBtnGo(self, event):  # wxGlade: servoControlFrame.<event_handler>
        servoName = self.txtServoName.GetValue()
        goalPos = int(self.txtServoPosition.GetValue())
        speed = int(self.txtServoSpeed.GetValue())
        if(servoName in self.servoCtrl.servoList):
            self.servoCtrl.setSpeed(servoName,speed)
            self.servoCtrl.setPosition(servoName,goalPos)
        self.updateServos()
        

    def onBtnGoStart(self, event):  # wxGlade: servoControlFrame.<event_handler>
        servoName = self.txtServoName.GetValue()
        speed = int(self.txtServoSpeed.GetValue())
        goalPos = self.servoCtrl.servoList[servoName]['StartPos']
        if(servoName in self.servoCtrl.servoList):
            self.servoCtrl.setSpeed(servoName,speed)
            self.servoCtrl.setPosition(servoName,goalPos)
        self.updateServos()

    def onBtnGoEnd(self, event):  # wxGlade: servoControlFrame.<event_handler>
        servoName = self.txtServoName.GetValue()
        speed = int(self.txtServoSpeed.GetValue())
        goalPos = self.servoCtrl.servoList[servoName]['EndPos']
        if(servoName in self.servoCtrl.servoList):
            self.servoCtrl.setSpeed(servoName,speed)
            self.servoCtrl.setPosition(servoName,goalPos)
        self.updateServos()

    def onClose(self, event):  # wxGlade: servoControlFrame.<event_handler>
        self.servoCtrl.closeServoPort()
        self.server.shutdown()
        event.Skip()
        





class servoApp(wx.App):
    def OnInit(self):
        self.frame = mainFrame(None, wx.ID_ANY, "")
        self.SetTopWindow(self.frame)
        self.frame.Show()
        return True

if __name__ == "__main__":
    gettext.install("Servo App")
    app = servoApp(0)
    app.MainLoop()
