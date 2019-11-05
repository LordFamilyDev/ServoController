#!/usr/bin/env python
# -*- coding: utf-8 -*-

################################################################################
# Copyright 2017 ROBOTIS CO., LTD.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
################################################################################

# Author: Ryu Woon Jung (Leon)

import time
import serial
import sys
import platform
import socket

LATENCY_TIMER = 16
DEFAULT_BAUDRATE = 1000000


class PortHandler(object):
    def __init__(self, port_name, port):
        self.is_open = False
        self.baudrate = DEFAULT_BAUDRATE
        self.packet_start_time = 0.0
        self.packet_timeout = 0.0
        self.tx_time_per_byte = 0.0

        self.is_using = False
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port_name = port_name
        self.port = port

    def openPort(self):
        self.socket.connect((self.port_name,self.port))
        self.is_open = True
        return True

    def closePort(self):
        self.socket.close()
        self.is_open = False

    def clearPort(self):
        pass

    def setPortName(self, port_name):
        self.port_name = port_name

    def getPortName(self):
        return self.port_name

    def setBaudRate(self, baudrate):
        self.baudrate = baudrate
        return True

    def getBaudRate(self):
        return self.baudrate

    # def getBytesAvailable(self):
    #     return self.ser.in_waiting

    def readPort(self, length):
        return self.socket.recv(length)

    def writePort(self, packet):
        return self.socket.send(bytes(packet))

    def setPacketTimeout(self, packet_length):
        self.packet_start_time = self.getCurrentTime()
        self.packet_timeout = (self.tx_time_per_byte * packet_length) + (LATENCY_TIMER * 2.0) + 2.0

    def setPacketTimeoutMillis(self, msec):
        self.packet_start_time = self.getCurrentTime()
        self.packet_timeout = msec

    def isPacketTimeout(self):
        if self.getTimeSinceStart() > self.packet_timeout:
            self.packet_timeout = 0
            return True

        return False

    def getCurrentTime(self):
        return round(time.time() * 1000000000) / 1000000.0

    def getTimeSinceStart(self):
        time_since = self.getCurrentTime() - self.packet_start_time
        if time_since < 0.0:
            self.packet_start_time = self.getCurrentTime()

        return time_since

    def setupPort(self, cflag_baud):
        if self.is_open:
            self.closePort()

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.is_open = True

        self.tx_time_per_byte = (1000.0 / self.baudrate) * 10.0

        return True

    def getCFlagBaud(self, baudrate):
        if baudrate in [9600, 19200, 38400, 57600, 115200, 230400, 460800, 500000, 576000, 921600, 1000000, 1152000,
                        2000000, 2500000, 3000000, 3500000, 4000000]:
            return baudrate
        else:
            return -1            
