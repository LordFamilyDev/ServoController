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
else:
    import sys, tty, termios
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    def getch():
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

from dynamixel_sdk import *                    # Uses Dynamixel SDK library

# Control table address for Dynamixel MX
ADDR_XL320_TORQUE_ENABLE       = 24               # Control table address is different in Dynamixel model
ADDR_XL320_MOVING_SPEED        = 32
ADDR_XL320_GOAL_POSITION       = 30
ADDR_XL320_PRESENT_POSITION    = 37
ADDR_XL320_IS_MOVING           = 49
ADDR_XL320_ERROR_STATUS        = 50

PROTOCOL_VERSION2           = 2.0

# Default setting
DXL1_ID                     = 2                 # Dynamixel#1 ID : 1
BAUDRATE                    = 1000000             # Dynamixel default baudrate : 57600
DEVICENAME                  = '192.168.30.158'    # Check which port is being used on your controller
PORT                        = 2001
                                                # ex) Windows: "COM1"   Linux: "/dev/ttyUSB0" Mac: "/dev/tty.usbserial-*"

TORQUE_ENABLE               = 1                 # Value for enabling the torque
TORQUE_DISABLE              = 0                 # Value for disabling the torque
DXL1_MINIMUM_POSITION_VALUE = 10           # Dynamixel will rotate between this value
DXL1_MAXIMUM_POSITION_VALUE = 1020            # and this value (note that the Dynamixel would not move when the position value is out of movable range. Check e-manual about the range of the Dynamixel you use.)
DXL1_MOVING_STATUS_THRESHOLD = 10



def main():
    # Initialize PortHandler instance
    # Set the port path
    # Get methods and members of PortHandlerLinux or PortHandlerWindows
    portHandler = PortHandler(DEVICENAME,PORT)

    # Initialize PacketHandler instance
    # Set the protocol version
    packetHandler = PacketHandler(PROTOCOL_VERSION2)


    # Open port
    if portHandler.openPort():
        print("Succeeded to open the port")
    else:
        print("Failed to open the port")
        print("Press any key to terminate...")
        getch()
        quit()


    # Set port baudrate
    try:
        if portHandler.setBaudRate(BAUDRATE):
            print("Succeeded to change the baudrate")
        else:
            print("Failed to change the baudrate")
            print("Press any key to terminate...")
            getch()
            quit()
    except:
        portHandler.closePort()

    index = 0
    dxl1_goal_position = [DXL1_MINIMUM_POSITION_VALUE, DXL1_MAXIMUM_POSITION_VALUE]         # Goal position of Dynamixel MX


    # Enable Dynamixel#1 Torque
    dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL1_ID, ADDR_XL320_TORQUE_ENABLE, TORQUE_ENABLE)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))
    else:
        print("Dynamixel#%d has been successfully connected" % DXL1_ID)

    while 1:
        print("Press any key to continue! (or press ESC to quit!)")
        if getch() == chr(0x1b):
            break

        # Write Dynamixel#1 goal position
        dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, DXL1_ID, ADDR_XL320_GOAL_POSITION, dxl1_goal_position[index])
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))


        while 1:
            # Read Dynamixel#1 present position
            dxl1_present_position, dxl_comm_result, dxl_error = packetHandler.read2ByteTxRx(portHandler, DXL1_ID, ADDR_XL320_PRESENT_POSITION)
            if dxl_comm_result != COMM_SUCCESS:
                print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
            elif dxl_error != 0:
                print("%s" % packetHandler.getRxPacketError(dxl_error))

            print("[ID:%03d] GoalPos:%03d  PresPos:%03d" % (DXL1_ID, dxl1_goal_position[index], dxl1_present_position))

            if not (abs(dxl1_goal_position[index] - dxl1_present_position) > DXL1_MOVING_STATUS_THRESHOLD):
                break

        # Change goal position
        if index == 0:
            index = 1
        else:
            index = 0


    # Disable Dynamixel#1 Torque
    dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL1_ID, ADDR_XL320_TORQUE_ENABLE, TORQUE_DISABLE)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))

    # Close port
    portHandler.closePort()
    pass

if __name__ == '__main__':
    main()
