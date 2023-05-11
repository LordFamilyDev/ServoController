import wx
import gettext
import threading
import queue
import time

from dynamixel_sdk import robotis_def
from servoControlAppGUI import servoControlFrame
from Servo import Servo
from UDPCommandListener import UDPServerThread, UDPDataHandler

import ServoConfig

NUM_RETRIES = 3
GOAL_ERROR = 20
RESET_DLY = 20

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

        self.resetFlag = False
        self.servoResetting = 0
        self.resetCount = RESET_DLY 

        self.servoUpdateRow = 0
        self.movingList = []

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
        self.updateMovers()
        self.updateServo(self.servoGrid.GetCellValue(self.servoUpdateRow,self.__gridColName))
        if(self.resetFlag):
            self.resetServos()
        self.servoUpdateRow += 1
        if(self.servoUpdateRow >= len(self.servoCtrl.servoList)): self.servoUpdateRow = 0
        pass
    
    def updateMovers(self):
        for servo in self.movingList:
            goal = self.servoCtrl.getGoalPosition(servo)
            pos = self.servoCtrl.getPosition(servo)
            if(goal-pos) < GOAL_ERROR:
                self.movingList.remove(servo)
                self.txtLog.AppendText("\nServo %s Motion Complete"%(servo))

    def parseCmd(self,cmd):
        print("Got:" + str(cmd))
        cmds = cmd.decode("utf-8").split("\n}")
        for c in cmds:
            c = c.strip(" 	{}")
            args = c.split(":")

            if(len(args) < 1): 
                print("no commands found")
                return

            if(args[0] == "Connect"):
                self.openPort()
                continue

            if(args[0] == "Enable"):
                self.enableServos()
                continue
            
            if(args[0] == "Disable"):
                self.disableServos()
                continue
            
            if(args[0] == "Reset"):
                self.txtLog.SetValue("Reseting Servo Positions...")
                self.resetFlag = True
                continue

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
            self.txtLog.SetValue("Moving %s to %s"%(servo,args[1]))
            self.servoCtrl.setSpeed(servo,speed)
            self.servoCtrl.setPosition(servo,position)
            self.movingList.append(servo)




    def onBtnOpenPorts(self, event):  # wxGlade: servoControlFrame.<event_handler>
        print("Opening Com Ports")
        self.openPort()

    def openPort(self):
        self.txtLog.SetValue("Connecting to Servo Control")
        retries = 0
        while True:
            retries += 1
            self.servoCtrl.openServoPort()
            if(self.servoCtrl.isConnected() or retries >= NUM_RETRIES):
                break
            time.sleep(1)
        if(not self.servoCtrl.isConnected()):
            self.txtLog.SetValue("Could not Connect to Servo Controller")
            return
        self.enableServos()
        self.updateServos()
        self.txtLog.SetValue("Servos connected Sucesfully!")
        

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
        eCount = 0
        s = self.servoCtrl
        for servo in s.servoList:
            retries = 0
            while True:
                retries += 1
                s.enableServo(servo )
                if('Torque' in s.servoList[servo]):
                    s.setTorque(servo,s.servoList[servo]['Torque'])
                if('PGain' in s.servoList[servo]):
                    s.setPGain(servo,s.servoList[servo]['PGain'])
                if('IGain' in s.servoList[servo]):
                    s.setIGain(servo,s.servoList[servo]['IGain'])
                if('DGain' in s.servoList[servo]):
                    s.setPGain(servo,s.servoList[servo]['DGain'])
                if('Punch' in s.servoList[servo]):
                    s.setPunch(servo,s.servoList[servo]['Punch'])

                if(s.isEnabled(servo)==1):
                    break
                if(retries >= NUM_RETRIES):
                    eCount +=1
                    self.txtLog.AppendText("\nServo %s not responding"%(servo))
                    break
        if(not eCount):
            self.txtLog.SetValue("Servo's Enabled Successfully")
            
        self.updateServos()
    
    def onClickDisableServos(self,event):
        self.disableServos()

    def disableServos(self):
        self.txtLog.SetValue("Disabling Servo's")
        eCount = 0
        s = self.servoCtrl
        for servo in s.servoList:
            retries = 0
            while True:
                retries += 1
                s.disableServo(servo )

                if(not s.isEnabled(servo)):
                    break

                if(retries >= NUM_RETRIES):
                    eCount +=1
                    self.txtLog.AppendText("\nServo %s not responding"%(servo))
                    break
        if(not eCount):
            self.txtLog.SetValue("Servo's Enabled Successfully")
        self.updateServos()



    def onClickResetServos(self, event):  # wxGlade: servoControlFrame.<event_handler>
        self.txtLog.SetValue("Reseting Servo Positions...")
        self.resetFlag = True

    def resetServos(self):
        if(self.resetCount < RESET_DLY):
            self.resetCount += 1
            return
        if(self.servoResetting >= len(self.servoCtrl.servoList)): 
            self.txtLog.AppendText("\nAll Servos Reset")
            self.servoResetting = 0
            self.resetCount = RESET_DLY
            self.resetFlag = False
            return

        self.resetCount = 0
        servo = self.servoGrid.GetCellValue(self.servoResetting,self.__gridColName)
        self.resetFlag = True
        s = self.servoCtrl
        self.txtLog.AppendText("\nResetting Servo %s"%(servo))
        s.setPosition(servo,s.servoList[servo]['StartPos'])
        self.movingList.append(servo)
        self.servoResetting += 1
        pass

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
            self.movingList.append(servoName)
        self.updateServos()
        

    def onBtnGoStart(self, event):  # wxGlade: servoControlFrame.<event_handler>
        servoName = self.txtServoName.GetValue()
        speed = int(self.txtServoSpeed.GetValue())
        goalPos = self.servoCtrl.servoList[servoName]['StartPos']
        if(servoName in self.servoCtrl.servoList):
            self.servoCtrl.setSpeed(servoName,speed)
            self.servoCtrl.setPosition(servoName,goalPos)
            self.movingList.append(servoName)
        self.updateServos()

    def onBtnGoEnd(self, event):  # wxGlade: servoControlFrame.<event_handler>
        servoName = self.txtServoName.GetValue()
        speed = int(self.txtServoSpeed.GetValue())
        goalPos = self.servoCtrl.servoList[servoName]['EndPos']
        if(servoName in self.servoCtrl.servoList):
            self.servoCtrl.setSpeed(servoName,speed)
            self.servoCtrl.setPosition(servoName,goalPos)
        self.updateServos()

    def onBtnEnableServo(self,event):
        servoName = self.txtServoName.GetValue()
        self.servoCtrl.enableServo(servoName)


    def onBtnDisableServo(self,event):
        servoName = self.txtServoName.GetValue()
        self.servoCtrl.disableServo(servoName)


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
