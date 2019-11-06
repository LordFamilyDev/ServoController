#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Lordy
#
# Created:     31/10/2019
# Copyright:   (c) Lordy 2019
# Licence:     <your licence>
#-------------------------------------------------------------------------------


import os

if os.name == 'nt':
    import msvcrt
    def getch():
        return msvcrt.getch().decode()
# else:
#     import sys, tty, termios
#     fd = sys.stdin.fileno()
#     old_settings = termios.tcgetattr(fd)
#     def getch():
#         try:
#             tty.setraw(sys.stdin.fileno())
#             ch = sys.stdin.read(1)
#         finally:
#             termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
#         return ch

from dynamixel_sdk import PacketHandler,TCPPortHandler,COMM_SUCCESS  # Uses Dynamixel SDK library
import ServoConfig

# Control table address for Dynamixel MX
ADDR_XL320_TORQUE_ENABLE       = 24               # Control table address is different in Dynamixel model
ADDR_XL320_MOVING_SPEED        = 32
ADDR_XL320_GOAL_POSITION       = 30
ADDR_XL320_PRESENT_POSITION    = 37
ADDR_XL320_IS_MOVING           = 49
ADDR_XL320_ERROR_STATUS        = 50
ADDR_XL320_HARDWARE_ERROR_STAT = 50
ADDR_XL320_TORQUE              = 41
ADDR_XL320_VOLTAGE             = 45
ADDR_XL320_TEMP                = 46

ADDR_XL320_VOLTAGE
ADDR_XL320_TEMP

PROTOCOL_VERSION               = 2.0

# Default setting
BAUDRATE                    = 1000000             # Dynamixel default baudrate : 57600
DEFAULTPORT                 = '192.168.30.158'    # Check which port is being used on your controller
                                                # ex) Windows: "COM1"   Linux: "/dev/ttyUSB0" Mac: "/dev/tty.usbserial-*"

TORQUE_ENABLE               = 1               # Value for enabling the torque
TORQUE_DISABLE              = 0               # Value for disabling the torque
MINIMUM_POSITION_VALUE      = 0               # Dynamixel will rotate between this value
MAXIMUM_POSITION_VALUE      = 1023            # and this value (note that the Dynamixel would not move when the position value is out of movable range. Check e-manual about the range of the Dynamixel you use.)
MIN_POSITION_DEG            = 0
MAX_POSITION_DEG            = 300
MIN_SPEED                   = 1
MAX_SPEED                   = 1023
DEFAULT_SPEED               = 0
MOVING_STATUS_THRESHOLD = 5

SERVO_STATUS = {
    0:'NotConnected',


}



class Servo:
    def __init__(self,port = ServoConfig.PORT):
        self.port = port
        self.packetHandler = PacketHandler(PROTOCOL_VERSION)
        self.portHandler = None
        self.servoList = ServoConfig.SERVO_LIST

    def isConnected(self):
        if(self.portHandler and self.portHandler.is_open):
            return True
        else:
            return False

    def openServoPort(self):
        self.portHandler = TCPPortHandler(self.port)
        self.portHandler.openPort()
    
    def closeServoPort(self):
        if(self.portHandler):
            self.portHandler.closePort()

    def ping(self,servoName):
        return self.packetHandler.ping(self.portHandler,self.servoList[servoName]['ID'])

    def pingAll(self):
        pass

    def getStatus(self,servoName):
        isHardwareError , comm_result, dxl_error = self.packetHandler.read1ByteTxRx(self.portHandler, self.servoList[servoName]['ID'], ADDR_XL320_HARDWARE_ERROR_STAT)
        if( comm_result != COMM_SUCCESS):
            return "Com Fail"
        if(isHardwareError):
            return "HW Error:"+ str(isHardwareError)
        torqueEnabled , comm_result, dxl_error = self.packetHandler.read1ByteTxRx(self.portHandler, self.servoList[servoName]['ID'], ADDR_XL320_TORQUE_ENABLE)
        if(comm_result != COMM_SUCCESS):
            return "Com Fail"
        if(torqueEnabled == 0):
            return "IDLE"
        isMoving , comm_result, dxl_error = self.packetHandler.read1ByteTxRx(self.portHandler, self.servoList[servoName]['ID'], ADDR_XL320_IS_MOVING)
        if(comm_result != COMM_SUCCESS):
            return "Com Fail"
        if(isMoving):
            return "MOVING"
        return "READY"

    def getPosition(self,servoName):
        position, comm_result, dxl_error = self.packetHandler.read2ByteTxRx(self.portHandler, self.servoList[servoName]['ID'], ADDR_XL320_PRESENT_POSITION)
        posDeg = round(position * (MAX_POSITION_DEG/MAXIMUM_POSITION_VALUE),1)
        if(comm_result == COMM_SUCCESS):
            return posDeg
        else:
            return -1

    def getTorque(self,servoName):
        torque, comm_result, dxl_error = self.packetHandler.read2ByteTxRx(self.portHandler, self.servoList[servoName]['ID'], ADDR_XL320_TORQUE)
        if(comm_result == COMM_SUCCESS):
            return torque
        else:
            return -1

    def getVoltage(self,servoName):
        voltage, comm_result, dxl_error = self.packetHandler.read2ByteTxRx(self.portHandler, self.servoList[servoName]['ID'], ADDR_XL320_VOLTAGE)
        if(comm_result == COMM_SUCCESS):
            return voltage/100
        else:
            return -1

    def getTemp(self,servoName):
        temp, comm_result, dxl_error = self.packetHandler.read2ByteTxRx(self.portHandler, self.servoList[servoName]['ID'], ADDR_XL320_TEMP)
        if(comm_result == COMM_SUCCESS):
            return temp
        else:
            return -1


# getTorque
# getVoltage
# getTemp

    def isMoving(self,servoName):
        return False

    def enableServo(self,servoName):
        return self.packetHandler.write1ByteTxRx(self.portHandler, self.servoList[servoName]['ID'], ADDR_XL320_TORQUE_ENABLE,1)

    def setSpeed(self,servoName,Speed):
        speed = int(Speed)
        if(speed < 0 or speed > 1023) : speed = 0
        return self.packetHandler.write2ByteTxRx(self.portHandler, self.servoList[servoName]['ID'], ADDR_XL320_MOVING_SPEED,speed)

    def setPosition(self,servoName,Position):
        if(Position < MIN_POSITION_DEG): Position = MIN_POSITION_DEG
        if(Position > MAX_POSITION_DEG): Position = MAX_POSITION_DEG
        pos = round(Position * MAXIMUM_POSITION_VALUE / MAX_POSITION_DEG)
        print("Moving Servo %s to Position %d°(%d)"%(servoName,Position,pos))
        return self.packetHandler.write2ByteTxRx(self.portHandler, self.servoList[servoName]['ID'], ADDR_XL320_GOAL_POSITION,pos)

MINIMUM_POSITION_VALUE      = 0               # Dynamixel will rotate between this value
MAXIMUM_POSITION_VALUE      = 1023            # and this value (note that the Dynamixel would not move when the position value is out of movable range. Check e-manual about the range of the Dynamixel you use.)
MIN_POSITION_DEG            = 0
MAX_POSITION_DEG            = 300



##  def main():

    # # Initialize PortHandler instance
    # # Set the port path
    # # Get methods and members of PortHandlerLinux or PortHandlerWindows
    # portHandler = PortHandler(DEVICENAME)

    # # Initialize PacketHandler instance
    # # Set the protocol version
    


    # # Open port
    # if portHandler.openPort():
    #     print("Succeeded to open the port")
    # else:
    #     print("Failed to open the port")
    #     print("Press any key to terminate...")
    #     getch()
    #     quit()


    # # Set port baudrate
    # try:
    #     if portHandler.setBaudRate(BAUDRATE):
    #         print("Succeeded to change the baudrate")
    #     else:
    #         print("Failed to change the baudrate")
    #         print("Press any key to terminate...")
    #         getch()
    #         quit()
    # except:
    #     portHandler.closePort()

    # index = 0
    # dxl1_goal_position = [DXL1_MINIMUM_POSITION_VALUE, DXL1_MAXIMUM_POSITION_VALUE]         # Goal position of Dynamixel MX


    # # Enable Dynamixel#1 Torque
    # dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL1_ID, ADDR_XL320_TORQUE_ENABLE, TORQUE_ENABLE)
    # if dxl_comm_result != COMM_SUCCESS:
    #     print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    # elif dxl_error != 0:
    #     print("%s" % packetHandler.getRxPacketError(dxl_error))
    # else:
    #     print("Dynamixel#%d has been successfully connected" % DXL1_ID)

    # while 1:
    #     print("Press any key to continue! (or press ESC to quit!)")
    #     if getch() == chr(0x1b):
    #         break

    #     # Write Dynamixel#1 goal position
    #     dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, DXL1_ID, ADDR_XL320_GOAL_POSITION, dxl1_goal_position[index])
    #     if dxl_comm_result != COMM_SUCCESS:
    #         print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    #     elif dxl_error != 0:
    #         print("%s" % packetHandler.getRxPacketError(dxl_error))


    #     while 1:
    #         # Read Dynamixel#1 present position
    #         dxl1_present_position, dxl_comm_result, dxl_error = packetHandler.read2ByteTxRx(portHandler, DXL1_ID, ADDR_XL320_PRESENT_POSITION)
    #         if dxl_comm_result != COMM_SUCCESS:
    #             print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    #         elif dxl_error != 0:
    #             print("%s" % packetHandler.getRxPacketError(dxl_error))

    #         print("[ID:%03d] GoalPos:%03d  PresPos:%03d" % (DXL1_ID, dxl1_goal_position[index], dxl1_present_position))

    #         if not (abs(dxl1_goal_position[index] - dxl1_present_position) > DXL1_MOVING_STATUS_THRESHOLD):
    #             break

    #     # Change goal position
    #     if index == 0:
    #         index = 1
    #     else:
    #         index = 0


    # # Disable Dynamixel#1 Torque
    # dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL1_ID, ADDR_XL320_TORQUE_ENABLE, TORQUE_DISABLE)
    # if dxl_comm_result != COMM_SUCCESS:
    #     print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    # elif dxl_error != 0:
    #     print("%s" % packetHandler.getRxPacketError(dxl_error))

    # # Close port
    # portHandler.closePort()
    # pass

# if __name__ == '__main__':
#     main()

