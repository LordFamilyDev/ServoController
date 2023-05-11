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
import sys
#import platform
import socket

LATENCY_TIMER = 16

SOCKET_TIMEOUT    = .100


class TCPPortHandler(object):
    def __init__(self, port):
        self.is_open = False
        self.packet_timeout = 0.0
        self.tx_time_per_byte = 0.0

        self.is_using = False
        self.socket = None
        self.port = port


    def openPort(self):
        print("Opening ",self.port)
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(SOCKET_TIMEOUT)
            self.socket.connect(self.port)
            self.is_open = True
            return True
        except Exception as e:
            print ("Port Open Failed with Exception: %s"%(e))
            del self.socket
            self.socket = None
            self.is_open = False

    def closePort(self):
        if(self.is_open):
            self.socket.close()
            del self.socket
            self.socket = None
        self.is_open = False

    def readPort(self, length):
        if(not self.is_open):
            return ""
        try:
            return self.socket.recv(length)
        except Exception as ex:
            #print("Reading...")
            #print(ex)
            # self.closePort()
            return ""

    def writePort(self, packet):
        if(not self.is_open):
            return 0
        try:
            return self.socket.send(bytes(packet))
        except Exception as ex:
            print(ex)
            return 0

    def clearPort(self):
        # timeout = self.socket.gettimeout()
        # try:
        #     self.socket.settimeout(0)
        #     self.socket.recv(1024)
        # finally:
        #     self.socket.settimeout(timeout)
        pass

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
        